import argparse
import pickle
import sqlite3
import dotenv
import psycopg2
import numpy as np
import time

from db_mgmt import db_mgmt
from scraper import scraper
from lda_app import create_docs, run_lda
from distance import lda_distance, size_features


def create_distance_db(conn, model, docs):
    '''
    Create a poem_distance table based on the lda model.

    :param conn: sqlite connection
    :param model: lda model
    :param docs: lda docs
    :return: None
    '''
    c = conn.cursor()

    print("getting all poems")
    all_poems = db_mgmt.get_values(conn, 'poetry', 'poem')

    # maybe this should be a dictionary of indeces: distance
    print("getting lda distance")
    indeces, lda_d = lda_distance.get_lda_distance(model, docs)

    # and this just changes the distance by adding the size feature
    print("getting size distance")
    size_d = size_features.get_size_distance(indeces, all_poems)

    print("finding closest poem for each and commiting to db")
    # this is so we get db indeces
    # each iteration of this loop is for a single poem
    w = .5  # weight for size feature
    for i in range(1910, len(all_poems) + 1):
        a = time.time()
        # close_poem = lda_distance.find_closest_doc(i, indeces, lda_d, size_d)
        # this is very very slow! speed it up in new implementation somehow...
        distances = [0]  # will contain distance values
        poem_i = [0]  # will contain index of poem that distance away
        check_poem = []  # will contain indeces of indeces with the curr poem in it
        for j in range(len(indeces)):
            if i in indeces[j]:
                check_poem.append(j)
        b = time.time()
        print("Part A: {}".format(b - a))  # this is the slow part
        for j in check_poem:
            distance = (1 - w) * lda_d[j] + w * size_d[j]
            if distance < min(distances):
                distances.append(distance)
                if indeces[j][0] == i:
                    poem_i.append(indeces[j][1])
                else:
                    poem_i.append(indeces[j][0])
        c = time.time()
        print("Part B: {}".format(c - b))
        index = distances.index(min(distances))
        close_poem = poem_i[index]
        # c.execute("UPDATE poetry SET close_poem=%s WHERE id=%s", (close_poem, i))
        # conn.commit()


def create_topic_table(conn, model, num_words):
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
    # c.execute(cmd)
    # conn.commit()

    columns = "("
    values = "("
    for i in range(num_words):
        columns += "word" + str(i) + ","
        values += "%s,"
    columns = columns[:-1] + ")"
    values = values[:-1] + ")"

    topic_word = model.topic_word_
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-num_words:-1]
        cmd = "INSERT INTO topics {} VALUES {}".format(columns, values)
        print(cmd)
        print(topic_words)
    #     c.execute(cmd, topic_words)
    # conn.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Put some data into database things!')
    parser.add_argument('--add_poems', action='store_true',
                        help='add poems to the poetry databse')
    parser.add_argument('--run_lda', action='store_true',
                        help='run lda on poems in current database')
    parser.add_argument('--print_lda', action='store_true',
                        help='print results of lda output stored in \
                        /temp/lda_out.p and save top topic words to db.')
    parser.add_argument('--get_distance', action='store_true',
                        help='get distance between poems in current database')
    parser.add_argument('-s', '--start_num', default=48000, type=int,
                        help='start num for adding poems')
    parser.add_argument('-e', '--end_num', default=48010, type=int,
                        help='end num for adding poems')

    args = parser.parse_args()

    # postgres on heroku connection
    dotenv.load()
    DATABASE = dotenv.get('DATABASE')
    USER = dotenv.get('DBUSER')
    HOST = dotenv.get('HOST')
    PASSWORD = dotenv.get('PASSWORD')
    cmd = "dbname='{}' user='{}' host='{}' password='{}'".format(DATABASE, USER, HOST, PASSWORD)
    conn = psycopg2.connect(cmd)
    c = conn.cursor()
    # c.execute('drop table if exists {}'.format('poetry'))
    # c.execute("CREATE TABLE poetry (id serial primary key, title text, poet text, url text, poem text, close_poem integer)")
    # conn.commit()

    if args.add_poems:
        base_url = 'https://www.poetryfoundation.org/poems-and-poets/poems/detail/'
        scraper.scrape_website(conn, 'poetry', base_url, args.start_num, args.end_num, print_output=True)
        db_mgmt.print_db_table_info(conn, 'poetry')

    if args.run_lda:
        docs, vocab = create_docs.get_docs(conn, 'poetry', stopwords=True)
        titles = db_mgmt.get_values(conn, 'poetry', 'title')

        model = run_lda.run_lda(docs)
        lda_out = (docs, vocab, titles, model)
        pickle.dump(lda_out, open('temp/lda_out.p', 'wb'))

        run_lda.print_lda_output(docs, model, vocab, titles)

    if args.print_lda:
        (docs, vocab, titles, model) = pickle.load(open('temp/lda_out.p', 'rb'))
        run_lda.print_lda_output(docs, model, vocab, titles)

        create_topic_table(conn, model, 8)

    if args.get_distance:
        (docs, vocab, titles, model) = pickle.load(open('temp/lda_out.p', 'rb'))
        create_distance_db(conn, model, docs)

    conn.close()
