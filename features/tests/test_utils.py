from features.tests.poem import poem, lines, words
from features import utils

def test_get_poem():
	expected = poem
	actual = utils.get_poem('features/tests/poem.txt')
	assert expected == actual


def test_get_lines():
	expected = lines
	actual = utils.get_lines(poem)
	assert expected == actual

def test_get_words():
	expected = words
	actual = utils.get_words(poem)
	assert expected == actual