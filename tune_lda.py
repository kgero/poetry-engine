import sqlite3
import dotenv
import psycopg2
import db_mgmt.db_mgmt as db_mgmt
import lda_app.create_docs as create_docs


dotenv.load()
DATABASE = dotenv.get('DATABASE')
USER = dotenv.get('DBUSER')
HOST = dotenv.get('HOST')
PASSWORD = dotenv.get('PASSWORD')
cmd = "dbname='{}' user='{}' host='{}' password='{}'".format(DATABASE, USER, HOST, PASSWORD)
conn = psycopg2.connect(cmd)
# conn = sqlite3.connect('poemdb2.db')

raw_docs = db_mgmt.get_values(conn, 'poetry', 'poem')
clean_docs = []
for doc in raw_docs:
    cleaned = create_docs.read_poem(doc)
    clean_docs.append(cleaned)

vocab_freq = create_docs.get_vocab_freq(clean_docs)
vocab_freq_doc = create_docs.get_vocab_freq(clean_docs, doc_freq=True)

print("Frequency of 'the': {}", vocab_freq['the'])
print("Num docs with 'the': {}", vocab_freq_doc['the'])

print("\nTop 25 most occuring words by frequency in corpus.")
d = vocab_freq
count = 25
i = 0
for w in sorted(d, key=d.get, reverse=True):
    i += 1
    if i > count:
        break
    print(w, d[w])

print("\nTop 25 most occuring words by number of documents seen in.")
d = vocab_freq_doc
count = 25
i = 0
for w in sorted(d, key=d.get, reverse=True):
    i += 1
    if i > count:
        break
    print(w, d[w])
