from scraper import scraper
import os

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def test_download_poems_erika_meitner():
	scraper.download_poems('erika-meitner')
	poems = ['TerraNullius', 'YizkerBukh', 'Yiddishland', 'StakingaClaim']
	for poem in poems:
		expected_p = 'test_data/poems/erika-meitner/'+poem+'.txt'
		actual_p = 'poems/erika-meitner/'+poem+'.txt'
		assert os.path.exists(expected_p)
		assert file_len(expected_p) == file_len(actual_p)
		with open(expected_p, 'r') as expected, open(actual_p, 'r') as actual:
			expected_l = expected.readline()
			actual_l = actual.readline()
			assert expected_l == actual_l


# def test_download_poems_walt_whitmean():
# 	scraper.download_poems('walt-whitman')
# 	poems = ['America', 'Areyouthenewpersondrawntowardme']
# 	for poem in poems:
# 		expected_p = 'test_data/poems/walt-whitman/'+poem+'.txt'
# 		actual_p = 'poems/walt-whitman/'+poem+'.txt'
# 		assert os.path.exists(expected_p)
# 		assert file_len(expected_p) == file_len(actual_p)
# 		with open(expected_p, 'r') as expected, open(actual_p, 'r') as actual:
# 			expected_l = expected.readline()
# 			actual_l = actual.readline()
# 			assert expected_l == actual_l



