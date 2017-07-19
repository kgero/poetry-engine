import numpy as np
import time

from db_mgmt import db_mgmt
from distance import lda_distance, utils


def add_close_poems(conn, model, docs, norm_attr, size_weight, num_poems=500):
    '''
    Add the closest poem to the poetry table based on the lda model
    and size features.

    TODO: add size features

    e.g. norm_attr = {"lda": {"mean": 3.5, "range": 10},
                      "size_length": {"mean": .1, "range": 100},
                      "size_width": {"mean": .1, "range": 100}}

    :param conn: psycog2 connection
    :param model: lda model
    :param docs: lda docs
    :param norm_attr: dictionary
    :param size_weight: float (between 0 and 1)
    :return: None
    '''
    c = conn.cursor()
    lda_u = norm_attr["lda"]["mean"]
    lda_r = norm_attr["lda"]["range"]
    w = size_weight

    # c.execute("ALTER TABLE poetry ADD COLUMN top_topic int DEFAULT NULL")
    # conn.commit()

    print("getting all poems")
    all_poems = db_mgmt.get_values(conn, 'poetry', 'poem')
    all_poems = all_poems[0:num_poems]
    a = time.time()

    # this is so we get db indeces
    # each iteration of this loop is for a single poem
    for i in range(1, len(all_poems) + 1):  # 1 indexed
        if i % 100 == 0:
            print("Finished with {} poems".format(i))
        best_distance = None
        best_poem = None
        for j in range(1, len(all_poems) + 1):  # 1 indexed
            if i == j:
                continue
            lda = lda_distance.lda_distance2(i - 1, j - 1, model)
            lda_n = utils.normalize_element(lda, lda_u, lda_r)
            distance = lda
            if best_distance is None:
                best_distance = distance
                best_poem = j
            elif distance < best_distance:
                best_distance = distance
                best_poem = j

        c.execute("UPDATE poetry SET close_poem=%s WHERE id=%s", (best_poem, i))

        topics = model.doc_topic_[i - 1]
        top_topic = int(np.where(topics == max(topics))[0][0]) + 1  # 1 indexed
        c.execute("UPDATE poetry SET top_topic=%s WHERE id=%s", (top_topic, i))

        conn.commit()


def create_topic_table(conn, model, vocab, num_words):
    '''
    Create a topics table based on the lda model.

    This function creates a table called 'topics' in which each row is a topic
    and each column is the word with the next highest probability. i.e. first
    row is word with highest probability, etc.

    :param conn: database connection
    :param model: lda model
    :param num_words: integer number of words i.e. columns
    :returns: none
    '''
    c = conn.cursor()
    c.execute('drop table if exists {}'.format('topics'))
    cmd = "CREATE TABLE topics (id serial primary key, "
    for i in range(num_words):
        cmd += "word" + str(i) + " text, "
    cmd = cmd[:-2]
    cmd += ")"
    print(cmd)
    c.execute(cmd)
    conn.commit()

    columns = "("
    values = "("
    for i in range(num_words):
        columns += "word" + str(i) + ","
        values += "%s,"
    columns = columns[:-1] + ")"
    values = values[:-1] + ")"

    topic_word = model.topic_word_
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:(-num_words - 1):-1]
        cmd = "INSERT INTO topics {} VALUES {}".format(columns, values)
        print(cmd)
        print(topic_words)
        c.execute(cmd, topic_words)
    conn.commit()


def print_best_topic(conn, poem):
    '''
    Print poem and top topic words. 

    :param conn: database connection
    :param poem: poem id (1 indexed for data base)
    :returns: none
    '''
    c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cmd = "SELECT * FROM {} WHERE id=%s".format(poem)
    c.execute(cmd)
    poems = c.fetchall()
    for p in poem:
        print(p['title'])
        print(p['poem'])
        print("")

        topic = p['top_topic']
