# Bot to simulate other users for clustering demo

import database, users
import time
from random import randint

bots = [("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox"),("apple", "mac"), ("microsoft", "windows"), ("music", "song"), ("samsung", "apple"), ("politics", "washington"), ("football", "sports"), ("technology", "google"), ("sports", "google"), ("apple", "google"), ("politics","htc"), ("kardashian","twitter"), ("htc","samsung"), ("twitter","android"), ("facebook","twitter"), ("detroit","syracuse"),("entertainment","movie"), ("film","pop"), ("game", "xbox") ]


def register():
	for i in range(0, len(bots)):
		users.add_user(str(i))


def read():
	d = database.Database()
	d.open()
	articles = d.fetch_articles_time_limit(int(time.time()) - 2*86400) #Fetch articles

	for i in range(0,len(bots)):
		print "Bot #", i
		for article in articles:
			# 20% chance that article is not read
			if randint(0,9) > 1 :
				if bots[i][0] in article[1] or bots[i][1] in article[1]:
					if randint(0,9) > 0:
						d.store_read_article(str(i), article[2], 1)
					else:
						d.store_read_article(str(i), article[2], -1)
				else:
					if randint(0,9) > 4:
						d.store_read_article(str(i), article[2], 1)
					else:
						d.store_read_article(str(i), article[2], -1)

if __name__ == '__main__':
	#register()
	read()