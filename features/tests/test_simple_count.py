from features.tests.poem import poem, lines, words, num_stanzas, num_lines, num_words
from features import simple_count

def test_num_words_in_line():
    expected = 8
    line = "Whose woods these are I think I know."
    actual = simple_count.num_words_in_line(line)
    assert actual == expected

def test_num_char_in_line():
	expected = 37
	line = "Whose woods these are I think I know."
	actual = simple_count.num_char_in_line(line)
	assert actual == expected

def test_num_letters_in_line():
	expected = 29
	line = "Whose woods these are I think I know."
	actual = simple_count.num_letters_in_line(line)
	assert actual == expected

def test_num_stanzas_in_poem():
	expected = num_stanzas
	actual = simple_count.num_stanzas_in_poem(poem)
	assert actual == expected

def test_num_lines_in_poem():
	expected = num_lines
	actual = simple_count.num_lines_in_poem(poem)
	assert actual == expected

def test_num_words_in_poem():
	expected = num_words
	actual = simple_count.num_words_in_poem(poem)
	assert actual == expected

def test_num_char_in_poem():
	expected = 0
	for line in lines:
		expected += simple_count.num_char_in_line(line)
	actual = simple_count.num_char_in_poem(poem)
	assert expected == actual

def test_num_letters_in_poem():
	expected = 0
	for word in words:
		word = ''.join(e for e in word if e.isalnum())
		expected += len(word)
	actual = simple_count.num_letters_in_poem(poem)
	assert expected == actual