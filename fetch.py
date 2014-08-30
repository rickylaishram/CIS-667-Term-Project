# coding: utf-8

# This script fetches the articles

import urllib2, feedparser, nltk, json, time
import database as db
import tfidf as tf
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import string, pprint
import cleanhtml

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ' '.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

# Remove non-alpha numeric, length 1 and stop words
def filter_words(words):
	word_list = []
	fstop = open('Smart.English.stop', 'r')
	stoptext = fstop.read()
	stopwords = nltk.wordpunct_tokenize(stoptext)
	for word in words:
		if word.isalpha() and (word.lower() not in stopwords) and (len(word) > 1) and (word.lower() not in word_list):
			word_list.append(word.lower())
	return word_list

def save_articles(articles):
	d = db.Database()
	d.open()
	d.store_articles(articles)
	d.close()

def update_wordsdoc(words):
	d = db.Database()
	d.open()
	d.store_words(words)
	d.close()

# Normalize total value of tfidf to 1
def normalize_tfidf(words):
	values = []
	total = 0.0
	for word in words:
		total += word[1]

	for word in words:
		values.append([word[0], word[1]/total])
	return values

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def fetch_articles(feed_list):	
	for (name, url) in feed_list.items():
		print "Fetching from "+name
		doc = feedparser.parse(url)
		print "Fetched "+str(len(doc.entries))+" items"

		for entry in doc.entries:
			entities = []
			words = []
			article = []
			try:
				#response = urllib2.urlopen(entry.link);
				#data = response.read()
				#content = strip_tags(removeNonAscii(data))
				links = string.split(entry.link, "http://")

				print links[2]
				response = urllib2.urlopen("http://"+links[2])
				html = response.read()
				
				cleaned = cleanhtml.cleanhtml(html,False)

				if len(cleaned) > 200 :
					#content = strip_tags(cleaned).encode('ascii', 'ignore')
					content = strip_tags(entry.description).encode('ascii', 'ignore')
					sents = nltk.sent_tokenize(content)

					words.extend(nltk.word_tokenize(entry.title))

					# Chunk each sentence
					for sent in sents:
						words.extend(nltk.word_tokenize(sent))

					words = filter_words(words)

					update_wordsdoc(words)

					t = tf.TFIDF()
					tfidf = t.assign_values(words)
					n_tfidf = normalize_tfidf(tfidf[:10])

					pp = pprint.PrettyPrinter(indent=4)
					pp.pprint(n_tfidf)

					article.append((int(time.time()), entry.title, links[2], json.JSONEncoder().encode(n_tfidf)))

					save_articles(article)
			except Exception, e:
				print e
			

	print "Fetched all"

if __name__ == '__main__':
	feed_list = {"Google Top News" : "https://news.google.com/news/feeds?output=rss", "Google World": "https://news.google.com/news/feeds?output=rss&topic=w", "Google Technology": "https://news.google.com/news/feeds?output=rss&topic=tc", "Google Bussiness": "https://news.google.com/news/feeds?output=rss&topic=e", "Google Entertainment": "https://news.google.com/news/feeds?output=rss&topic=e", "Google Sports": "https://news.google.com/news/feeds?output=rss&topic=s", "Google Science": "https://news.google.com/news/feeds?output=rss&topic=snc", "Google Spotlight" : "https://news.google.com/news/feeds?output=rss&topic=ir", "Google Health" : "https://news.google.com/news/feeds?output=rss&topic=m", }
	#bing_list = {Bing Top News": "http://www.bing.com/news/?format=RSS", "Bing US News": "http://www.bing.com/news?q=us+news&FORM=NSBABR&format=RSS", "Bing World News": "http://www.bing.com/news?q=world+news&FORM=NSBABR&format=RSS", "Bing Entertainment News": "http://www.bing.com/news?q=entertainment+news&FORM=NSBABR&format=RSS", "Bing Sci/Tech News": "http://www.bing.com/news?q=science+technology+news&FORM=NSBABR&format=RSS", "Bing Bussiness News": "http://www.bing.com/news?q=business+news&FORM=NSBABR&format=RSS", "Bing Political News": "http://www.bing.com/news?q=political+news&FORM=NSBABR&format=RSS", "Bing Sports News": "http://www.bing.com/news?q=sports+news&FORM=NSBABR&format=RSS", "Bing Health News": "http://www.bing.com/news?q=health+news&FORM=NSBABR&format=RSS}
	fetch_articles(feed_list)