from features.get_features import features

def get_weights(data, poem):
	"""
	Returns a list of data dictionary objects where each object contains the name of the poem,
	the name of the poet, and the 'connective weight' between that poem and the poem passed
	into the function.

	The 'connective weight' is the average of the absolute value of the difference between
	features of the two specified poems.
	"""
	for item in data:
		item['weight'] = get_connective_weight(item, poem)
	return data

def get_connective_weight(poem1, poem2):
	"""
	Returns the connective weight between the two poems. Each poem must be a data dict object
	with title, poet, and features specified.
	"""
	w = 0
	for feature in features:
		f1 = poem1['features'][feature]
		f2 = poem2['features'][feature]
		w+= abs(f1-f2)
	return w