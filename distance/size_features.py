import re

from distance import utils


def get_num_lines(poem_text):
    '''
    Return number of lines.

    :param poem_text: str
    :return: float
    '''
    return float(len(poem_text.split('\n')) - 1)


def get_num_words(poem_text):
    '''
    Return number of words.

    :param poem_test: str
    :return: float
    '''
    x = re.sub('\n+', ' ', poem_text).strip().split(' ')
    return float(len(x))


def get_size_features(all_poems):
    '''
    Return corresponding list of num_lines and list of num_words.

    :param all_poems: list of str
    :return: list of float, list of float
    '''
    num_words = []
    num_lines = []
    for poem in all_poems:
        num_words.append(get_num_words(poem))
        num_lines.append(get_num_lines(poem))
    return num_lines, num_words

def get_size_distance(index_tuples, all_poems):
    '''
    Return list of normalized size distance.

    index_tuples are db indexes, i.e. start at 1. python lists start at 0,
    so minus one from index_tuples to get all_poems indce.

    :param index_tuples: list of tuples
    :param all_poems: list of str
    :return: list of float
    '''
    word_distances = []
    line_distances = []

    print("get features")
    num_lines, num_words = get_size_features(all_poems)

    print("size distance pass one")
    for t in index_tuples:
        lines1 = num_lines[t[0] - 1]
        lines2 = num_lines[t[1] - 1]
        words1 = num_words[t[0] - 1]
        words2 = num_words[t[1] - 1]
        word_distances.append((words1 - words2)**2)
        line_distances.append((lines1 - lines2)**2)

    print("feature normalizatio")
    word_distances = utils.normalize_feature(word_distances)
    line_distances = utils.normalize_feature(line_distances)

    print("size distance pass two")
    distances = []
    for i, w in enumerate(word_distances):
        l = line_distances[i]
        distances.append(w + l)

    return utils.normalize_feature(distances)
