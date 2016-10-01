import lda
import numpy as np


def run_lda(docs, n_topics=20, n_iter=1500, print_output=False):
    '''
    Return lda model.

    :param docs: lda doc array
    :param n_topics: int
    :param n_iter: int
    :return: model
    '''

    if print_output:
        print('Document dimensions:')
        print(docs.shape)

    model = lda.LDA(n_topics=n_topics, n_iter=n_iter, random_state=1)
    model.fit(docs)

    return model


def print_lda_output(docs, model, vocab, titles):

    print(".components_ : ", model.components_.shape)
    print(".doc_topic_ : ", model.doc_topic_.shape)
    print(".topic_word_ : ", model.topic_word_.shape)
    print("docs : ", docs.shape)
    print("vocab : ", len(vocab))
    print("titles : ", len(titles))

    topic_word = model.topic_word_
    n_top_words = 8

    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    doc_topic = model.doc_topic_

    for i in range(10):
        print(titles[i])
        print(doc_topic[i])
