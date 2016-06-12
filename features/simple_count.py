
def num_words_in_line(line):
	words = line.split(' ')
	return len(words)

def num_char_in_line(line):
	return len(line)

def num_letters_in_line(line):
	fresh_line = ''.join(e for e in line if e.isalnum())
	return len(fresh_line)

def num_stanzas_in_poem(poem):
	num_stanzas = 1
	lines = poem.split('\n')
	for line in lines:
		if len(line) == 0:
			num_stanzas += 1
	return num_stanzas

def num_lines_in_poem(poem):
	lines = poem.split('\n')
	num_lines = 0
	for line in lines:
		if len(line) != 0:
			num_lines += 1
	return num_lines

def num_words_in_poem(poem):
	poem = poem.replace('\n', ' ')
	num = 0
	for word in poem.split(' '): 
		if word:
			num += 1
	return num

def num_char_in_poem(poem):
	poem = poem.replace('\n', '')
	return len(poem)

def num_letters_in_poem(poem):
	# faster w regex?
	fresh_poem = ''.join(e for e in poem if e.isalnum())
	return len(fresh_poem)
