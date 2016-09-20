import pickle
import random

import lda

from lda_app.create_docs import get_docs
from lda_app.get_distance import get_distance, find_close_docs

import numpy as np

from scraper import scraper

RUN_SCRAPER = False
RUN_LDA = False
LOAD_LAST_LDA = True
PRINT_LDA_OUTPUT = True
GET_DISTANCE = True

if RUN_SCRAPER:
    scraper.download_poems('louise-gluck')

if RUN_LDA:
    docs, vocab, titles, poets, urls = get_docs("poems")

    print('Document dimensions:')
    print(docs.shape)

    model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
    model.fit(docs)
    topic_word = model.topic_word_
    n_top_words = 8

    documents = (docs, vocab, titles, poets, urls)
    pickle.dump(documents, open("temp/documents.p", "wb"))
    pickle.dump(model, open("temp/model.p", "wb"))


if LOAD_LAST_LDA:
    docs, vocab, titles, poets, urls = pickle.load(open("temp/documents.p", "rb"))
    model = pickle.load(open("temp/model.p", "rb"))
    topic_word = model.topic_word_
    n_top_words = 8


if PRINT_LDA_OUTPUT:
    print(".components_ : ", model.components_.shape)
    print(".doc_topic_ : ", model.doc_topic_.shape)
    print(".topic_word_ : ", model.topic_word_.shape)
    print("docs : ", docs.shape)
    print("vocab : ", len(vocab))
    print("titles : ", len(titles))

    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    doc_topic = model.doc_topic_

    for i in range(10):
        print(titles[i])
        print(doc_topic[i])

if GET_DISTANCE:
    get_distance(1, 2, model)

    doc = random.randrange(len(docs))
    close_docs, close_rms = find_close_docs(doc, model)
    print("Closest poems to {} by {}".format(titles[doc], poets[doc]))
    for i in range(len(close_docs)-1, -1, -1):
        print("{} by {}\t{}".format(titles[close_docs[i]], poets[close_docs[i]], close_rms[i]))
        print(urls[close_docs[i]])
