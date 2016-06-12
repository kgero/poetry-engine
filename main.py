from features import get_features

feature_dict = get_features.apply('features/tests/poem.txt')

for key in feature_dict:
	print key, '\t', feature_dict[key]