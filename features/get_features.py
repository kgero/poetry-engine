from features import simple_count, utils

features = {
	'#stanzas': simple_count.num_stanzas_in_poem,
	'#lines': simple_count.num_lines_in_poem,
	'#words': simple_count.num_words_in_poem,
	'#char': simple_count.num_char_in_poem,
	'#letters': simple_count.num_letters_in_poem
	}

def apply(filepath):
	poem = utils.get_poem(filepath)
	poem_features = {}
	for feature in features:
		poem_features[feature] = features[feature](poem)
	return poem_features