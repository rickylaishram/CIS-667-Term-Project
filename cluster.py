# Uses kNN clustering to find nearest neighbors
# Returns the resultant probabilities

import database
import pprint

pp = pprint.PrettyPrinter(indent=4)

class Cluster(object):
	"""docstring for ClassName"""
	def __init__(self, k, name, cutoff):
		super(Cluster, self).__init__()
		self.k = k
		self.name = name
		self.cutoff = cutoff
		self.neighbors = []
		
	def find_neighbours(self):
		d = database.Database()
		d.open()

		# Fetch all users from articles_status table
		neighbors = d.fetch_all_users_from_status()

		# Fetch articles user have read
		user_read = d.fetch_last_k_read_urls(self.name, self.cutoff)
		user_statuses = []
		for item in user_read:
			user_statuses.append((item[1],item[3]))

		neighbors_score = []

		for neighbor in neighbors:
			if neighbor is not self.name:
				read = d.fetch_last_k_read_urls(neighbor, self.cutoff)

				# Small positive number to prevent division by 0 error
				positive_score = 0.01
				negative_score = 0.01
				for item in read:
					if (item[1],item[3]) in user_statuses:
						positive_score += 1
					elif (item[1], -1*item[3]) in user_statuses:
						negative_score += 1
				neighbors_score.append((item[2], positive_score/(positive_score+negative_score)))
		
		# Find the k-nearest neighbors (highest neighbor scores)
		neighbors_score.sort(key=lambda tup: tup[1], reverse=True)

		self.neighbors = neighbors_score[:self.k]
		d.close()

		print "---k Nearest Neighbors---"
		print "name/similarity/status"
		pp.pprint(self.neighbors)

	def get_probability(self, url):
		d = database.Database()
		d.open()

		k_neighbor_score = []
		like = 0.01
		dislike = 0.01
		for item in self.neighbors:
			article_status = d.fetch_user_article_status(item[0], url)

			if article_status is not None:
				k_neighbor_score.append((item[0], item[1], article_status[3]))
				if(article_status[3] == 1):
					like += item[1]
				else:
					dislike += item[1]

		# (like, probability)
		probability = (like/(like+dislike), dislike/(like+dislike))
		d.close()

		print "---k Nearest Neighbors probabilties---"
		print "name/similarity/status"
		pp.pprint(k_neighbor_score)

		print "---Probability from clustering---"
		print "like/dislike"
		pp.pprint(probability)

		return probability


def main():
	cl = Cluster(50,'ricky',100)
	cl.find_neighbours()
	cl.get_probability('www.usatoday.com/story/news/nation/2013/12/13/health-flu-mental-alcohol/4008969/')


if __name__ == '__main__':
	main()
