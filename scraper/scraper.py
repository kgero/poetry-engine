# based on https://github.com/eli8527/poetryfoundation-scraper/

from bs4 import BeautifulSoup
from urllib.request import urlopen
import html
import re
import os


def download_poems(poet):
	if not os.path.exists(os.path.join('poems', poet)):
		os.mkdir(os.path.join('poems', poet))

	url = "http://www.poetryfoundation.org/poems-and-poets/poets/detail/"+poet+"#about"
	page = urlopen(url)
	soup = BeautifulSoup(page.read(), "html.parser")

	# this ignores .*/resources/learning/core-poems/detail/.* poems
	poems = soup.find_all('a', href=re.compile('.*/poems-and-poets/poems/detail/.*'))

	# the first returned url has http:, the others start at //www. 
	# i ... don't know why
	found_poems = []
	for poem in poems:
		poem_url = poem.get('href')
		if 'http:' not in poem_url:
			poem_url = 'http:' + poem_url
		if poem_url not in found_poems:
			poem_page = urlopen(poem_url)
			poem_soup = BeautifulSoup(poem_page.read(), "html.parser")
			
			poem_title = poem_soup.find('span', {'class': 'hdg hdg_1'})

			if poem_title:
				title = html.parser.unescape(poem_title.text).encode('utf8')
				title = title.decode('utf8')
				title = ''.join(e for e in title if e.isalnum())

				found_poems.append(poem_url)

				poem_content = poem_soup.find_all('div', {'class': 'poem'})
				filepath = 'poems/' + poet + '/' + title + '.txt'
				output = open(filepath, 'w')
				for content in poem_content:
					for line in content.find_all('div'):
						text = html.parser.unescape(line.text).encode('utf8')
						out = text.decode('utf8')
						print(out, file=output)

				output.close()
				print('')
