from features import get_features
import os

def apply(path):
	"""
	Returns a list of dictionary data objects, where each object has the data
	for a specific poem. i.e.

	data = [{
		title: 'America',
		poet: 'Walt Whitman',
		features: {
			'num_stanzas_in_poem'': 1
			'num_lines_in_poem': 5,
			'num_words_in_poem': 50,
			'num_char_in_poem': 200,
			'num_letters_in_poem': 180
			}
		},
		{
		title: 'America',
		poet: 'Walt Whitman',
		features: {
			'num_stanzas_in_poem'': 1
			'num_lines_in_poem': 5,
			'num_words_in_poem': 50,
			'num_char_in_poem': 200,
			'num_letters_in_poem': 180
			}
		}]

	path is the path to a folder of poems with structure:

	poems/
		walt-whitman/
			America.txt
			AGlimpse.txt
		erika-meitner/
			StakingaClaim.txt
			TerraNullius.txt
	"""
	data = []
	poets = []
	for item in os.listdir(path):
		if os.path.isdir(os.path.join(path, item)):
			poets.append(item)

	for poet in poets:
		full_path = os.path.join(path, poet)
		for poem in os.listdir(full_path):
			poem_path = os.path.join(full_path, poem)
			features = get_features.apply(poem_path)
			poem_data = {
				'title': poem.split('.')[0],
				'poet': poet,
				'features': features
				}
			data.append(poem_data)
	return data

def normalize_features(data):
	"""
	Returns data with all features normalized: (feature - u)/r
	"""
	for feature in get_features.features:
		feature_vals = []
		for item in data:
			feature_vals.append(item['features'][feature])
		u = sum(feature_vals)/float(len(feature_vals))
		r = max(feature_vals) - min(feature_vals)
		for item in data:
			f = float(item['features'][feature])
			item['features'][feature] = (f - u)/r
	return data