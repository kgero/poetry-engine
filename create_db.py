import sqlite3

from lda_app.run_lda import run_lda
from lda_app.get_distance import get_distance

documents, model = run_lda("poems")
docs, vocab, titles, poets, urls = documents


conn = sqlite3.connect('poem_info.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE poems
             (poem_num int, title text, poet text, url text)''')

for i in range(len(docs)):
    vals = (i, titles[i], poets[i], urls[i])
    # Insert a row of data
    c.execute("INSERT INTO poems VALUES (?,?,?,?)", vals)

# Save (commit) the changes
conn.commit()

c.execute('''CREATE TABLE poem_distances
             (poem1 int, poem2 int, distance real)''')

for i in range(len(docs)):
    for j in range(i + 1, len(docs)):
        rms = get_distance(i, j, model)
        vals = (i, j, rms)
        c.execute("INSERT INTO poem_distances VALUES (?,?,?)", vals)
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
