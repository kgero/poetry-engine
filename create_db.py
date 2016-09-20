import sqlite3

from lda_app.run_lda import run_lda
from lda_app.get_distance import find_close_docs

documents, model = run_lda("poems")
docs, vocab, titles, poets, urls = documents


conn = sqlite3.connect('example.db')

c = conn.cursor()

# Create table
# c.execute('''CREATE TABLE poems
#              (title, poet, url, c1, d1)''')

for i in range(len(docs)):
    close_docs, close_rms = find_close_docs(i, model)
    vals = (titles[i], poets[i], urls[i], close_docs[-1], close_rms[-1])
    # Insert a row of data
    c.execute("INSERT INTO poems VALUES (?,?,?,?,?)", vals)

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
