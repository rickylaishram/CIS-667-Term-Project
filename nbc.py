from __future__ import division
import database, json

class NaiveBayesClassifier(object):

	"""docstring for NaiveBayesClassifier"""
	def __init__(self, user, prior_like, prior_dislike, smoothing_factor=0.01):
		super (NaiveBayesClassifier, self).__init__()
		self.user = user
		self.likes, self.dislikes = self.fetch_likes_dislikes()
		self.prior_like = prior_like
		self.prior_dislike = prior_dislike
		self.smoothing_factor = smoothing_factor

	def fetch_likes_dislikes(self):
		d = database.Database()
		d.open()
		likes = d.fetch_user_likes(self.user)
		dislikes = d.fetch_user_dislikes(self.user)
		d.close()

		return likes, dislikes

	# Neumerator for probability of the word being in Like
	def probability_like(self, word):
		probability = 1

		if word in self.likes:
			probability = (self.likes[word][0] + self.smoothing_factor)
		else:
			probability = (self.smoothing_factor)
		return probability

	# Neumerator for probaility of the word being in dislike
	def probability_dislike(self, word):
		probability = 1

		if word in self.dislikes:
			probability = (self.dislikes[word][0] + self.smoothing_factor)
		else:
			probability = (self.smoothing_factor)
		return probability

	# Neumerator for probability of the word being in Like count based
	def probability_like_count(self, word):
		probability = 1

		if word in self.likes:
			probability = (self.likes[word][1] + self.smoothing_factor)
		else:
			probability = (self.smoothing_factor)
		return probability

	# Neumerator for probaility of the word being in dislike count based
	def probability_dislike_count(self, word):
		probability = 1

		if word in self.dislikes:
			probability = (self.dislikes[word][1] + self.smoothing_factor)
		else:
			probability = (self.smoothing_factor)
		return probability

	# Converts the probaility ratio to seperate probabilities 
	def convert_to_probability(self, ratio):
		probability_like = ratio/(1+ratio)
		probability_dislike = 1/(1+ratio)
		return round(probability_like,4), round(probability_dislike,4)

	def calculate_probability(self, url):
		p_like = 0.0
		p_dislike = 0.0
		p_like_c = 0.0
		p_dislike_c = 0.0

		d = database.Database()
		d.open()
		articles = d.fetch_article(url)

		if len(articles) > 0:
			print "---Keywords probabilities---"
			print "word/likes/dislikes"

			keywords = json.JSONDecoder().decode(articles[0][3])
			p_ratio = self.prior_like/self.prior_dislike
			p_ratio_c = self.prior_like/self.prior_dislike

			for word in keywords:
				likes = self.probability_like(word[0])
				dislikes = self.probability_dislike(word[0])
				p_ratio *= likes/dislikes
				p_ratio_c *= self.probability_like_count(word[0])/self.probability_dislike_count(word[0])

				print word[0], self.convert_to_probability(likes/dislikes)

			p_like, p_dislike = self.convert_to_probability(p_ratio)
			p_like_c, p_dislike_c = self.convert_to_probability(p_ratio_c)

		d.store_nbc_probability(self.user, url, {'p_like': p_like, 'p_dislike': p_dislike, 'p_like_c': p_like_c, 'p_dislike_c': p_dislike_c})
		d.close()

		return (p_like, p_dislike), (p_like_c, p_dislike_c)

def main():
	print "Nope!"
	#nbc = NaiveBayesClassifier('ricky', 0.5, 0.5)
	#d = database.Database()
	#d.open()
	#articles = d.fetch_all_articles()
	#d.close()

	#for article in articles:
	#	print article[1]
	#	print nbc.calculate_probability(article[2])

if __name__ == '__main__':
	main()