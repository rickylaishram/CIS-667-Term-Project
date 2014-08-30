import sqlite3, time, json

class Database(object):

	"""The Database class"""
	
	def __init__(self):		
		#super(Database, self).__init__()
		self.connection = None
		self.cursor = None

	def open(self):
		self.connection = sqlite3.connect('cis667TermProject.db')
		self.cursor = self.connection.cursor()
	
	# Setup the database
	def set_up(self):
		# Create articles table
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS articles 
			(time integer not null, title text not null, url text not null unique, keywords text)''')

		# Table that contains all the words and the number of docs
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS worddocs 
			(time integer not null, word text not null unique, docs integer not null)''')

		# Table that contains all the usernames
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS users 
			(time integer not null, name text not null unique)''')

		# Table that contains likes or dislikes by users for articles
		# 1 is like, -1 is dislike
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS article_status 
			(time integer not null, url text not null, name text not null, status integer not null)''')

		# Table that contains words and count of likes by user
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS likes
			(name text not null, words integer not null)''')

		# Table that contains words and count of dislikes by user
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS dislikes
			(name text not null, words integer not null)''')

		# Table that contains the probabilities calculated by NBC
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS nbc_probabilities 
			(time integer not null, url text not null, name text not null, probabilities integer not null)''')

		self.connection.commit()

	# Drop all the tables
	def drop_all(self):
		self.cursor.execute('''DROP TABLE IF EXISTS articles''')
		self.cursor.execute('''DROP TABLE IF EXISTS users''')
		self.cursor.execute('''DROP TABLE IF EXISTS likes''')
		self.cursor.execute('''DROP TABLE IF EXISTS dislikes''')
		self.cursor.execute('''DROP TABLE IF EXISTS worddocs''')
		self.cursor.execute('''DROP TABLE IF EXISTS article_status''')
		self.connection.commit()

	# CLose the db connection
	def close(self):
		self.connection.close()

	# Store article
	# Argument is a list of (time, title, url, keywords)
	def store_articles(self, articles):
		self.cursor.executemany('INSERT OR IGNORE INTO articles VALUES (?,?,?,?)', articles)
		self.connection.commit()

	# Store a new user
	def store_user(self, name):
		self.cursor.execute('INSERT OR IGNORE INTO users VALUES (?, ?)', (int(time.time()), name))
		words = {}
		jqords = json.JSONEncoder().encode(words)
		self.cursor.execute('INSERT OR IGNORE INTO likes VALUES (?, ?)', (name, jqords))
		self.cursor.execute('INSERT OR IGNORE INTO dislikes VALUES (?, ?)', (name, jqords))
		self.connection.commit()

	# Add to word list
	def store_words(self, words):
		data = self.fetch_all_words()

		# Remove repeated words
		filtered_words = []
		for word in words:
			if word not in filtered_words:
				filtered_words.append(word)

		for word in filtered_words:
			if word in data.keys():
				count = data[word] + 1
				self.cursor.execute('UPDATE worddocs SET docs = ? WHERE word = ?', (count, word))
			else:
				self.cursor.execute('INSERT OR IGNORE INTO worddocs VALUES (?, ?, ? )', (int(time.time()), word, 1) )
		self.connection.commit()

	# Add to likes
	def store_like(self, user, url):
		articles = self.fetch_article(url)
		likes = self.fetch_user_likes(user)
		if len(articles) > 0:
			words = json.JSONDecoder().decode(articles[0][3])
			for word in words:
				if word[0] in likes.keys():
					#likes[word[0]] += word[1]
					likes[word[0]] = (likes[word[0]][0] + word[1], likes[word[0]][1] + 1)
				else:
					#likes[word[0]] = word[1]
					likes[word[0]] = (word[1], 1)
			self.cursor.execute('UPDATE likes SET words = ? WHERE name = ?', (json.JSONEncoder().encode(likes), user))
			self.connection.commit()
		else:
			print "Error"

	# Add to dislikes
	def store_dislike(self, user, url):
		articles = self.fetch_article(url)
		dislikes = self.fetch_user_dislikes(user)
		if len(articles) > 0:
			words = json.JSONDecoder().decode(articles[0][3])
			for word in words:
				if word[0] in dislikes.keys():
					#dislikes[word[0]] += word[1]
					dislikes[word[0]] = (dislikes[word[0]][0] + word[1], dislikes[word[0]][1] + 1)
				else:
					#dislikes[word[0]] = word[1]
					dislikes[word[0]] = (word[1], 1)
			self.cursor.execute('UPDATE dislikes SET words = ? WHERE name = ?', (json.JSONEncoder().encode(dislikes), user))
			self.connection.commit()
		else:
			print "Error"

	def store_read_article(self, user, url, status):
		self.cursor.execute('INSERT OR IGNORE INTO article_status VALUES (?, ?, ?, ?)', (int(time.time()), url, user, status))
		self.connection.commit()
		if int(status) == 1 :
			self.store_like(user, url)
		elif int(status) == -1:
			self.store_dislike(user, url)

	def store_nbc_probability(self, user, url, probabilities):
		self.cursor.execute('INSERT OR IGNORE INTO nbc_probabilities VALUES (?, ?, ?, ?)', (int(time.time()), url, user, json.JSONEncoder().encode(probabilities)))
		self.connection.commit()

	#Fetch all nbc_probabilities for user
	def fetch_user_nbc_probabilities(self, user):
		nbclist = []
		probabilities = self.cursor.execute('SELECT DISTINCT * FROM nbc_probabilities WHERE name = "%s"' %user)
		for probability in probabilities:
			nbclist.append(probability)
		return nbclist

	def fetch_user_articles_statuses(self, user):
		article_list = []
		url_list = []
		articles = self.cursor.execute('SELECT DISTINCT * FROM article_status WHERE name = "%s"' %user)
		for article in articles:
			if article[1] not in url_list:
				article_list.append(article)
				url_list.append(article[1])
		
		return article_list

	# Fetch user likes
	def fetch_user_likes(self, user):
		likes = self.cursor.execute('SELECT * FROM likes WHERE name = "%s"' %user)
		return json.JSONDecoder().decode(likes.fetchone()[1])

	# Fetch user dislikes
	def fetch_user_dislikes(self, user):
		dislikes = self.cursor.execute('SELECT * FROM dislikes WHERE name = "%s"' %user)
		return json.JSONDecoder().decode(dislikes.fetchone()[1])

	# Fetch one article
	def fetch_article(self, url):
		article_list = []
		articles = self.cursor.execute('SELECT * FROM articles WHERE url = "%s"' %url)
		for article in articles:
			article_list.append(article)
		return article_list

	# Fetch user read articles
	def fetch_read_articles_url(self, name):
		article_list = []
		articles = self.cursor.execute('SELECT * FROM article_status WHERE name = "%s"' %name)
		for article in articles:
			article_list.append(article[1])
		return article_list

	# Fetch articles status read by user
	def fetch_user_article_status(self, name, url):
		query = self.cursor.execute('SELECT * FROM article_status WHERE name = "%s" AND url = "%s"' %(name,url))
		return query.fetchone()

	# Fetches all the articles
	def fetch_all_articles(self):
		article_list = []
		articles = self.cursor.execute('SELECT * FROM articles')
		for article in articles:
			article_list.append(article)
		return article_list

	# Fetch all users
	def fetch_all_users(self):
		users_list = []
		users = self.cursor.execute('SELECT * FROM users')
		for user in users:
			users_list.append(user)
		return users_list

	# Fetch all users
	def fetch_all_reads(self):
		articles_list = []
		articles = self.cursor.execute('SELECT * FROM article_status')
		for article in articles:
			articles_list.append(article)
		return articles_list

	# Fetch all words
	# Returns dict
	def fetch_all_words(self):
		word_list = {}
		words = self.cursor.execute('SELECT * FROM worddocs')
		for word in words:
			word_list[word[1]] = word[2]
		return word_list

	# Fetch articles before specified time
	def fetch_articles_time_limit(self, before):
		article_list = []
		articles = self.cursor.execute('SELECT * FROM articles WHERE time > %s' %before)
		for article in articles:
			article_list.append(article)
		return article_list

	# Check if user exist
	def user_exist(self, name):
		exist = False;
		if len(self.cursor.execute('SELECT * FROM users WHERE name = "%s"' %name).fetchall()) > 0:
			exist = True
		return exist

	# FUnctions below this deals with multiple users
	def fetch_all_users_from_status(self):
		usernames = []
		statuses = self.cursor.execute('SELECT * FROM article_status')
		for status in statuses:
			if status[2] not in usernames:
				usernames.append(status[2])
		return  usernames

	def fetch_last_k_read_urls(self, username, k):
		urls = []
		read_list = self.cursor.execute('SELECT * FROM article_status WHERE name="%s" ORDER BY time DESC LIMIT "%s"' %(username,k))
		return read_list.fetchall();

def main():
	#print "Nope!"
	d = Database()
	d.open()
	#usernames = d.fetch_all_users_read("www.chicagotribune.com/sns-rt-heart-arrest-20131119,0,5550745.story")
	urls = d.fetch_last_k_read_urls("8", "10")
	for di in urls:
		print di
	d.close()


if __name__ == '__main__':
	main()