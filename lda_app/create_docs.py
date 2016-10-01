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

import re
import string

import numpy as np


def get_features(words, word_list):
    '''
    Return a word_dict and updated word_list.

    :param words: str (words are space separated)
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


def read_poem(poem):
    '''
    Return a cleaned string.

    Returned string is all lower case with punctuation and line feeds removed.

    :param path: str
    :return: str
    '''
    trnsltr1 = str.maketrans({key: None for key in string.punctuation + '’'})
    trnsltr2 = str.maketrans('\n', ' ')

    clean_str = poem.translate(trnsltr1).translate(trnsltr2).lower()
    clean_str = re.sub(' +', ' ', clean_str)
    clean_str = clean_str.strip()

    return clean_str


def lexicalize(raw_docs):
    '''
    Return a document array based on raw_docs, a list of cleaned strings.

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


def get_docs(conn, table):
    '''
    Return docs, for all entries in databse table from col 'poem'.

    :param conn: sqlite conn
    :param table: str
    :return: array, list
    '''
    raw_docs = []

    c = conn.cursor()
    c.execute('SELECT rowid,* FROM {}'.format(table))
    all_rows = c.fetchall()
    for row in all_rows:
        poem = row[4]
        clean_poem = read_poem(poem)
        raw_docs.append(clean_poem)

    docs, vocab = lexicalize(raw_docs)
    return docs, vocab


def get_titles(conn, table):
    '''
    Return list of titles from table of poetry.

    :param conn: sqlite connection
    :param table: str
    :return: list
    '''
    titles = []
    c = conn.cursor()
    c.execute('SELECT rowid,* FROM {}'.format(table))
    all_rows = c.fetchall()
    for row in all_rows:
        title = row[1]
        titles.append(title)
    return titles
