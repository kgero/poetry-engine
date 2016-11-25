from lda_app.create_docs import get_features, lexicalize, read_poem, get_vocab_freq

import numpy as np


def test_get_features():
    test_words = (
        'centre of equal daughters equal sons all all alike endeard grown')
    expected_word_dict = {
        'centre': 1, 'of': 1, 'equal': 2, 'daughters': 1,
        'sons': 1, 'all': 2, 'alike': 1, 'endeard': 1, 'grown': 1}
    expected_word_list = ['centre', 'of', 'equal', 'daughters', 'sons', 'all',
                          'alike', 'endeard', 'grown']

    # With empty provided word_list
    actual_word_dict, actual_word_list = get_features(test_words, [])
    assert actual_word_list == expected_word_list
    assert actual_word_dict == expected_word_dict

    # With prior unique words
    prior_words = ['who', 'are', 'you']
    expected_word_list_1 = prior_words + expected_word_list
    actual_word_dict, actual_word_list = get_features(test_words, prior_words)
    assert actual_word_list == expected_word_list_1
    assert actual_word_dict == expected_word_dict

    # With prior repeate words
    prior_words = ['who', 'centre', 'of']
    expected_word_list_2 = ['who'] + expected_word_list
    actual_word_dict, actual_word_list = get_features(test_words, prior_words)
    assert actual_word_list == expected_word_list_2
    assert actual_word_dict == expected_word_dict


def test_read_poem():
    poem = '1\nWhat is it, this you want!?\n\nno now\n'
    expected_str = '1 what is it this you want no now'
    actual_str = read_poem(poem)

    assert actual_str == expected_str

    poem = 'is this it? and i you?'
    expected_str = 'this you'
    actual_str = read_poem(poem, stopwords=True)

    assert actual_str == expected_str

    poem = 'is this it? and i you?'
    expected_str = 'is this it and i you'
    actual_str = read_poem(poem, stopwords=False)

    assert actual_str == expected_str

    poem = "“i love you!"
    expected_str = "i love you"
    actual_str = read_poem(poem, stopwords=False)

    assert actual_str == expected_str


def test_lexicalize():
    raw_docs = [
        'hey hey who are you',
        'hey i am just a person',
        'i am you']

    expected_array = np.array([
        [2, 1, 1, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 1, 1, 0, 0, 0]])
    expected_word_list = ['hey', 'who', 'are', 'you', 'i', 'am', 'just', 'a', 'person']
    actual_array, actual_word_list = lexicalize(raw_docs)
    assert actual_array.all() == expected_array.all()
    assert actual_word_list == expected_word_list


def test_get_vocab_freq():
    strings = [
        'hey hey who are you',
        'hey person',
        'hey you']

    expected_vocab_freq = {
        'hey': 4,
        'who': 1,
        'are': 1,
        'you': 2,
        'person': 1}

    actual_vocab_freq = get_vocab_freq(strings)
    assert actual_vocab_freq == expected_vocab_freq

    expected_vocab_freq = {
        'hey': 3,
        'who': 1,
        'are': 1,
        'you': 2,
        'person': 1}

    actual_vocab_freq = get_vocab_freq(strings, doc_freq=True)
    assert actual_vocab_freq == expected_vocab_freq
