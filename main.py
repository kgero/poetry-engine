import argparse
import pickle
import sqlite3
import dotenv
import psycopg2

from db_mgmt import db_mgmt, create_db
from scraper import scraper
from lda_app import create_docs, run_lda
from distance import lda_distance, utils


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
                        help='find closest poems and add to database')
    parser.add_argument('--get_normalization', action='store_true',
                        help='get normalization values for features')
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
        print("getting documents...")
        docs, vocab = create_docs.get_docs(conn, 'poetry', stopwords=True)
        titles = db_mgmt.get_values(conn, 'poetry', 'title')

        print("running lda...")
        model = run_lda.run_lda(docs)
        lda_out = (docs, vocab, titles, model)
        pickle.dump(lda_out, open('temp/lda_out.p', 'wb'))

        run_lda.print_lda_output(docs, model, vocab, titles)

    if args.print_lda:
        (docs, vocab, titles, model) = pickle.load(open('temp/lda_out.p', 'rb'))
        run_lda.print_lda_output(docs, model, vocab, titles)

        create_db.create_topic_table(conn, model, vocab, 20)

    if args.get_normalization:
        print("loading lda model...")
        (docs, vocab, titles, model) = pickle.load(open('temp/lda_out.p', 'rb'))

        print("getting lda distances...")
        i, lda_d = lda_distance.get_lda_distance(model, docs, normalize=False)

        print("getting normalization attributes...")
        norm_attr = {}
        norm_attr["lda"] = utils.get_norm_attr(lda_d)
        pickle.dump(norm_attr, open('temp/norm_attr.p', 'wb'))

        print("\nnorm_attr:{}".format(norm_attr))

    if args.get_distance:
        print("loading lda model and norm_attr...")
        (docs, vocab, titles, model) = pickle.load(open('temp/lda_out.p', 'rb'))
        norm_attr = pickle.load(open('temp/norm_attr.p', 'rb'))

        print("finding the closest poems. at 3850 poems, this takes about 15 minutes...")
        create_db.add_close_poems(conn, model, docs, norm_attr, 0, len(titles))

    conn.close()
