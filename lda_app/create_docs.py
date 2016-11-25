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

from db_mgmt import db_mgmt

stop_words = ['the', 'and', 'of', 'a', 'an', 'to', 'with', 'that', 'on', 'is', 'it', 'in', 'i', 'as', 'for', 'from', 'are']


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


def read_poem(poem, stopwords=False):
    '''
    Return a cleaned string.

    Returned string is all lower case with punctuation and line feeds removed.

    :param path: str
    :return: str
    '''
    # idea: could lemma-lize words...
    trnsltr1 = str.maketrans({key: None for key in string.punctuation + '’“'})
    trnsltr2 = str.maketrans('\n', ' ')

    clean_str = poem.translate(trnsltr1).translate(trnsltr2).lower()

    if stopwords:
        words = clean_str.split()
        keepwords = [word for word in words if word not in stop_words]
        clean_str = ' '.join(keepwords)

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


def get_docs(conn, table, stopwords=False):
    '''
    Return docs, for all entries in databse table from col 'poem'.

    :param conn: sqlite conn
    :param table: str
    :return: array, list
    '''
    raw_docs = db_mgmt.get_values(conn, table, 'poem')
    if len(raw_docs) == 0:
        raise('0 documents found.')
    clean_docs = []
    for doc in raw_docs:
        cleaned = read_poem(doc, stopwords=stopwords)
        clean_docs.append(cleaned)
    docs, vocab = lexicalize(clean_docs)
    return docs, vocab


def get_vocab_freq(strings, doc_freq=False):
    '''
    Return dict of vocab frequency for all strings.

    Key is the word, value is num times seen if doc_freq=False.
    Key is the word, value is num docs seen in if doc_freq=True.
    This is used for determing stop words to be filtered out.

    :param strings: list of str
    :return: dict
    '''
    vocab_freq = {}
    for doc in strings:
        cleaned = read_poem(doc)
        word_dict, word_list = get_features(cleaned, [])
        for word in word_dict:
            if word in vocab_freq:
                if not doc_freq:
                    vocab_freq[word] += word_dict[word]
                else:
                    vocab_freq[word] += 1
            else:
                if not doc_freq:
                    vocab_freq[word] = word_dict[word]
                else:
                    vocab_freq[word] = 1
    return vocab_freq
