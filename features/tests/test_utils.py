from test_data import america, generic_poem
from features import utils


def test_get_poem():
	expected = generic_poem.poem
	actual = utils.get_poem('test_data/generic_poem.txt')
	assert expected == actual

def test_get_whitman_poem():
	expected = america.poem
	actual = utils.get_poem('test_data/poems/walt-whitman/America.txt')
	assert expected == actual

def test_get_lines():
	poem = generic_poem.poem
	expected = generic_poem.lines
	actual = utils.get_lines(poem)
	assert expected == actual

def test_get_words():
	poem = generic_poem.poem
	expected = generic_poem.words
	actual = utils.get_words(poem)
	assert expected == actual