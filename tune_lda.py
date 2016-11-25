import sqlite3
import dotenv
import psycopg2
import pickle
import db_mgmt.db_mgmt as db_mgmt
import lda_app.run_lda as run_lda
import lda_app.create_docs as create_docs


def get_top_words():
    '''
    Print top occuring words in corpus.
    '''
    raw_docs = db_mgmt.get_values(conn, 'poetry', 'poem')
    clean_docs = []
    for doc in raw_docs:
        cleaned = create_docs.read_poem(doc)
        clean_docs.append(cleaned)

    vocab_freq = create_docs.get_vocab_freq(clean_docs)
    vocab_freq_doc = create_docs.get_vocab_freq(clean_docs, doc_freq=True)

    print("Frequency of 'the': {}", vocab_freq['the'])
    print("Num docs with 'the': {}", vocab_freq_doc['the'])

    print("\nTop 100 most occuring words by frequency in corpus.")
    d = vocab_freq
    count = 100
    i = 0
    for w in sorted(d, key=d.get, reverse=True):
        i += 1
        if i > count:
            break
        print(w, d[w])

    print("\nTop 100 most occuring words by number of documents seen in.")
    d = vocab_freq_doc
    count = 100
    i = 0
    for w in sorted(d, key=d.get, reverse=True):
        i += 1
        if i > count:
            break
        print(w, d[w])


def same_top_topics():
    close_poems = db_mgmt.get_values(conn, 'poetry', 'close_poem')
    (docs, vocab, titles, model) = pickle.load(open('temp/lda_out_small.p', 'rb'))

    count_top = 0  # num poems with same top topic
    count_good = 0  # num poems with top topic in top 3
    total_poems = 0  # num poems looked at
    for i in range(500):
        print("{}\t{}".format(i, close_poems[i]))
        if close_poems[i] is None:
            continue
        if close_poems[i] > 500:
            print("fuck")
            continue
        top_topics1 = run_lda.get_top_topics(i + 1, model)
        top_topics2 = run_lda.get_top_topics(close_poems[i], model)
        if top_topics1[0] == top_topics2[0]:
            count_top += 1
        else:
            print(model.doc_topic_[i])
            print(model.doc_topic_[close_poems[i] - 1])
        if top_topics1[0] in top_topics2[0:3]:
            count_good += 1
        total_poems += 1

    print("Total poems: {}\n \
        Total w shared top topic: {}\n \
        Total w shared top 3 topics: {}".format(
        total_poems, count_top, count_good))

if __name__ == "__main__":
    dotenv.load()
    DATABASE = dotenv.get('DATABASE')
    USER = dotenv.get('DBUSER')
    HOST = dotenv.get('HOST')
    PASSWORD = dotenv.get('PASSWORD')
    cmd = "dbname='{}' user='{}' host='{}' password='{}'".format(DATABASE, USER, HOST, PASSWORD)
    conn = psycopg2.connect(cmd)

    get_top_words()
    # same_top_topics()
