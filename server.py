from flask import Flask
from flask import *
import database as db
import nbc as classifier
import time, json, urllib2
from bs4 import BeautifulSoup
import re, json, random
import cleanhtml
import cluster

app = Flask(__name__)

@app.route('/')
def hello_world():
	f = open('html/webpage.html', 'r')
	html = f.read()
	f.close()
	return html

@app.route('/login', methods=['POST'])
def login():
	name = request.form['username']
	d = db.Database()
	d.open()
	exist = d.user_exist(name)
	d.close()
	return str(exist)

@app.route('/add_read', methods=['POST'])
def add_read():
	name = request.form['username']
	url = request.form['url']
	status = request.form['status']

	d = db.Database()
	d.open()
	d.store_read_article(name, url, status)
	d.close()
	return status

@app.route('/results')
def results():
	f = open('html/results.html', 'r')
	html = f.read()
	f.close()
	return html

@app.route('/get_results', methods=['POST'])
def get_results():
	name = request.form['username']

	d = db.Database()
	d.open()
	probabilities = d.fetch_user_nbc_probabilities(name)
	statuses = d.fetch_user_articles_statuses(name)
	d.close()

	data = []
	count = 0
	step = 0

	#number of time nbc_w and nbc_c was right
	nbc_w = 0
	nbc_c = 0
	total = 0

	for status in statuses:
		try:
			url = status[1]
			l = status[3]

			# Find from probabilities that match url
			for probability in probabilities:
				if (url == probability[1]) or ('http://'+url == probability[1]) or (url == 'http://'+probability[1]):

					p_data = json.JSONDecoder().decode(probability[3])
					
					if not (p_data["p_like"] == p_data["p_dislike"]) or not (p_data["p_like_c"] == p_data["p_dislike_c"]):

						total += 1
						#print total, p_data

						if (p_data["p_like"] > p_data["p_dislike"]) and (l > 0):
							nbc_w += 1
						if (p_data["p_like_c"] > p_data["p_dislike_c"]) and (l > 0):
							nbc_c += 1
						if (p_data["p_like"] < p_data["p_dislike"]) and (l < 0):
							nbc_w += 1
						if (p_data["p_like_c"] < p_data["p_dislike_c"]) and (l < 0):
							nbc_c += 1
						data.append([total, total, nbc_w, nbc_c])
						break

			count +=1
			if count % 1 == 0 :
				step +=1
				#data.append([step, total, nbc_w, nbc_c])

		except Exception, e:
			raise e
	#print data
	return json.JSONEncoder().encode(data)

@app.route('/get_article', methods=['POST'])
def read():
	name = request.form['username']
	d = db.Database()
	d.open()
	articles = d.fetch_articles_time_limit(int(time.time()) - 2*86400)[::-1] #Fetch articles in the last 2*24 hours
	read = d.fetch_read_articles_url(name)
	nbc = classifier.NaiveBayesClassifier(name, 0.5, 0.5, 0.0001)
	#cl = cluster.Cluster(25,name,100)
	#cl.find_neighbours()

	url = ""
	keywords = ""
	p_nbc_like = 0
	p_nbc_dislike = 0
	p_nbc_like_c = 0
	p_nbc_dislike_c = 0
	p_cl_like = 0
	p_cl_diskile = 0

	total_p_like = 0

	weight_nbc, weight_cluster = 0.8, 0.2

	for article in articles:
		if article[2] not in read:
			print "---URL---"
			print article[2]

			print "--Naive Bayes Classifier---"
			(nbc_like, nbc_dislike), (nbc_like_c, nbc_dislike_c) = nbc.calculate_probability(article[2])
			print "like/dislike"
			print nbc_like, nbc_dislike

			print "---k Nearest Neighbor Cluster---"
			#cl_like, cl_dislike = cl.get_probability(article[2])
			cl_like, cl_dislike = 0.5, 0.5

			# Add of getting random article
			#rnd = (time.time()%10 == 0)
			rnd = True
			#rnd = False
			if (weight_cluster*cl_like + weight_nbc*nbc_like > total_p_like) or rnd:
				total_p_like = weight_cluster*cl_like + weight_nbc*nbc_like 

				url = article[2]
				keywords = article[3]
				p_nbc_like = nbc_like
				p_nbc_dislike = nbc_dislike
				p_nbc_like_c = nbc_like_c
				p_nbc_dislike_c = nbc_dislike_c
				p_cl_like = cl_like
				p_cl_diskile = cl_dislike

				if rnd:
					break

	response = urllib2.urlopen("http://"+url)
	html = response.read()
	
	cleaned = cleanhtml.cleanhtml(html,True)

	return json.JSONEncoder().encode({'url':url, 'keywords':keywords, 'p_like': p_nbc_like, 'p_dislike': p_nbc_dislike, 'p_like_c': p_nbc_like_c, 'p_dislike_c': p_nbc_dislike_c, 'page':cleaned, 'cl_like':p_cl_like, 'cl_dislike':p_cl_diskile, 'weight_nbc': weight_nbc, 'weight_cluster': weight_cluster})
	#return json.JSONEncoder().encode(read)

if __name__ == '__main__':
	app.debug = True
	app.run()