import re
import codecs

def get_poem(filepath):
	'''Returns a str w contents of poem from file.'''
	lines = []
	with codecs.open(filepath, 'r', 'utf-8') as f:
		lines = f.readlines()
	poem = ""
	for line in lines:
		line = line.strip() + '\n'
		poem += line
	return poem.strip('\n')

def get_lines(poem):
	'''Returns lines in poem as a list of str.'''
	lines = poem.split('\n')
	fresh_lines = []
	for line in lines:
		if line:
			fresh_lines.append(line)
	return fresh_lines

def get_words(poem):
	'''Returns words in poem as a list of str.'''
	return re.findall(r"[\w']+", poem)