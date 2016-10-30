import argparse
import pickle
import sqlite3

from db_mgmt import db_mgmt
from scraper import scraper
from lda_app import create_docs, run_lda
from distance import lda_distance, size_features

# from lda_app.run_lda import run_lda
# from lda_app.get_distance import get_distance

# documents, model = run_lda("poems")
# docs, vocab, titles, poets, urls = documents


# conn = sqlite3.connect('poem_info.db')

# c = conn.cursor()

# # Create table
# c.execute('''CREATE TABLE poems
#              (poem_num int, title text, poet text, url text)''')

# for i in range(len(docs)):
#     vals = (i, titles[i], poets[i], urls[i])
#     # Insert a row of data
#     c.execute("INSERT INTO poems VALUES (?,?,?,?)", vals)

# # Save (commit) the changes
# conn.commit()

# c.execute('''CREATE TABLE poem_distances
#              (poem1 int, poem2 int, distance real)''')

def create_distance_db(conn, model, docs):
    '''
    Create a poem_distance table based on the lda model.

    :param conn: sqlite connection
    :param model: lda model
    :param docs: lda docs
    :return: None
    '''
    c = conn.cursor()
    c.execute('drop table if exists {}'.format('poem_distances'))
    c.execute("CREATE TABLE poem_distances (id integer primary key, poem1 int, poem2 int, distance real)")
    conn.commit()

    print("getting all poems")
    all_poems = db_mgmt.get_values(conn, 'poetry', 'poem')

    print("getting lda distance")
    indeces, lda_d = lda_distance.get_lda_distance(model, docs)

    print("getting size distance")
    size_d = size_features.get_size_distance(indeces, all_poems)

    print("commiting to db")
    for i in range(len(indeces)):
        vals = (indeces[i][0], indeces[i][1], lda_d[i] + size_d[i])
        c.execute("INSERT INTO poem_distances VALUES (null, ?,?,?)", vals)
    conn.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Put some data into database things!')
    parser.add_argument('--add_poems', action='store_true',
                        help='add poems to the poetry databse')
    parser.add_argument('--run_lda', action='store_true',
                        help='run lda on poems in current database')
    parser.add_argument('--print_lda', action='store_true',
                        help='print results of lda output stored in /temp/lda_out.p')
    parser.add_argument('--get_distance', action='store_true',
                        help='get distance between poems in current database')
    parser.add_argument('-s', '--start_num', default=48000, type=int,
                        help='start num for adding poems')
    parser.add_argument('-e', '--end_num', default=48010, type=int,
                        help='end num for adding poems')

    args = parser.parse_args()
    conn = sqlite3.connect('poemdb2.db')
    c = conn.cursor()
    # c.execute('drop table if exists {}'.format('poetry'))
    # c.execute("CREATE TABLE poetry (id integer primary key, title text, poet text, url text, poem text)")
    # conn.commit()

    if args.add_poems:
        base_url = 'https://www.poetryfoundation.org/poems-and-poets/poems/detail/'
        scraper.scrape_website(conn, 'poetry', base_url, args.start_num, args.end_num, print_output=True)
        db_mgmt.print_db_table_info(conn, 'poetry')

    if args.run_lda:
        docs, vocab = create_docs.get_docs(conn, 'poetry')
        titles = db_mgmt.get_values(conn, 'poetry', 'title')

        model = run_lda.run_lda(docs)
        lda_out = (docs, vocab, titles, model)
        pickle.dump(lda_out, open('temp/lda_out.p', 'wb'))

        run_lda.print_lda_output(docs, model, vocab, titles)

    if args.print_lda:
        (docs, vocab, titles, model) = pickle.load(open('temp/lda_out.p', 'rb'))
        run_lda.print_lda_output(docs, model, vocab, titles)

    if args.get_distance:
        (docs, vocab, titles, model) = pickle.load(open('temp/lda_out.p', 'rb'))
        create_distance_db(conn, model, docs)

    conn.close()
