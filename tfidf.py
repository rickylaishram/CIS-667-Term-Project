import database as db
import math, operator

class TFIDF(object):

	"""docstring for ClassName"""
	def __init__(self):
		super(TFIDF, self).__init__()

	# Takes a lis of words and returns a dict with word
	# number of docs its is present in
	def word_counts(self, words):
		count = {}
		for word in words:
			if word in count:
				count[word] += 1
			else:
				count[word] = 1
		return count
		
	# Caluclates the tf-idf values of words
	def idfList(self, words):
		values = {}

		d = db.Database()
		d.open()
		word_list = d.fetch_all_words()
		article_list = d.fetch_all_articles()
		d.close()

		for word in words:
			if len(word) > 1:
				tf = math.log(words[word] + 1)
				# 1 added because current doc also have the word
				idf = math.log(float(len(article_list) + 1)/float((word_list[word] + 1)))
				tfidf = tf*idf
				values[word] = tfidf
		return values

	# Assign values
	def assign_values(self, words):
		count = self.word_counts(words)
		data = self.idfList(count)
		tfidf = sorted(data.items(), key = operator.itemgetter(1), reverse=True)
		return tfidf