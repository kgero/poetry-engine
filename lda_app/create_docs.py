"""
Contains functions for generating a document representation of all .txt files
found in a directory. Document representation is an array of size num_files x
num_unique_words in which each entry is the number of times a word appears
in a file.

Temporary data forms:

Per file:
word_dict = dict{"word1": count, "word2": count}

Per directory:
word_list = [word1, word2, word3]
"""

import os
import string

import numpy as np


def get_features(words, word_list):
    '''
    Returns a word_dict and updated word_list.

    :param words: str
    :param word_list: list
    :return: dict, list
    '''
    word_dict = dict()
    for word in words.split(' '):
        if word not in word_dict:
            word_dict[word] = 1
            if word not in word_list:
                word_list.append(word)
        else:
            word_dict[word] += 1
    return word_dict, word_list


def read_poem(path):
    '''
    Returns a cleaned string, all lower case, punctuation removed.

    :param path: str
    :return: str
    '''
    trnsltr1 = str.maketrans({key: None for key in string.punctuation + '’'})
    trnsltr2 = str.maketrans('\n', ' ')
    clean_str = ''

    with open(path, 'r') as f:
        for line in f:
            clean_str += line.translate(trnsltr1).translate(trnsltr2).lower()
    return clean_str


def lexicalize(raw_docs):
    '''
    Returns a document array based on raw_docs, a list of cleaned strings.

    :param raw_docs: list
    :return: array
    '''
    word_list = []
    doc_list = []
    for doc in raw_docs:
        word_dict, word_list = get_features(doc, word_list)
        doc_list.append(word_dict)

    documents = np.zeros((len(doc_list), len(word_list)), dtype=np.int)

    for i, word_dict in enumerate(doc_list):
        for j, word in enumerate(word_list):
            if word in word_dict:
                documents[i, j] = word_dict[word]

    return documents, word_list


def get_docs(directory):
    '''
    Returns docs, vocab, and doc names based on all text files in directory.

    :param directory: str
    :return: array, list, list
    '''
    raw_docs = []
    doc_names = []

    for root, subdir, files in os.walk(directory):
        if root.count(os.path.sep) == 1:
            for name in files:
                path = os.path.join(root, name)
                doc_names.append(name[0:-4])
                raw_docs.append(read_poem(path))

    docs, vocab = lexicalize(raw_docs)
    return docs, vocab, doc_names
