import pickle

import lda

from lda_app.create_docs import get_docs
from lda_app.get_distance import get_distance

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
    docs, vocab, titles = get_docs("poems")

    print('Document dimensions:')
    print(docs.shape)

    model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
    model.fit(docs)
    topic_word = model.topic_word_
    n_top_words = 8

    documents = (docs, vocab, titles)
    pickle.dump(documents, open("temp/documents.p", "wb"))
    pickle.dump(model, open("temp/model.p", "wb"))


if LOAD_LAST_LDA:
    docs, vocab, titles = pickle.load(open("temp/documents.p", "rb"))
    model = pickle.load(open("temp/model.p", "rb"))
    topic_word = model.topic_word_
    n_top_words = 8


if PRINT_LDA_OUTPUT:
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    doc_topic = model.doc_topic_
    for i in range(10):
        print(titles[i])
        print(doc_topic[i])

if GET_DISTANCE:
    get_distance(1, 2, model)
