from features import simple_count, utils

features = {
	'num_stanzas_in_poem': simple_count.num_stanzas_in_poem,
	'num_lines_in_poem': simple_count.num_lines_in_poem,
	'num_words_in_poem': simple_count.num_words_in_poem,
	'num_char_in_poem': simple_count.num_char_in_poem,
	'num_letters_in_poem': simple_count.num_letters_in_poem
	}

def apply(filepath):
	poem = utils.get_poem(filepath)
	poem_features = {}
	for feature in features:
		poem_features[feature] = features[feature](poem)
	return poem_features