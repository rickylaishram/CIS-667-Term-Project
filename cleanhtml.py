from bs4 import BeautifulSoup
import re

# Extracts non content frompage
def cleanhtml(document, pretty=True):
	soup = BeautifulSoup(document)
	to_extract = soup.findAll('script')
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll('noscript')
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll('style')
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll('link')
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll('head')
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll('li')
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll('ul')
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll('img')
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll('input')
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll('iframe')
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll('submit')
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(id=re.compile('sidebar', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('sidebar', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(id=re.compile('head', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('head', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(id=re.compile('foot', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('foot', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(id=re.compile('comment', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('comment', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(id=re.compile('breadcrumb', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('breadcrumb', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(id=re.compile('video', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('video', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(id=re.compile('banner', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('banner', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(id=re.compile('share', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('share', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(id=re.compile('widget', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('widget', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(id=re.compile('recommend', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('recommend', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(id=re.compile('slideshow', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('slideshow', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('sponsor', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('sponsor', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('advertisement', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('advertisement', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('twitter', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('twitter', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('fb', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('fb', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('facebook', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('facebook', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('brand', re.I))
	for item in to_extract:
		item.extract()
	to_extract = soup.findAll(class_=re.compile('brand', re.I))
	for item in to_extract:
		item.extract()

	result = soup.prettify()

	if(not pretty) :
		result = soup.get_text()

	return result
