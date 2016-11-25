"""Functions for inserting and retrieving data from a database."""
import sqlite3
import psycopg2
import psycopg2.extras


def print_db_table_info(conn, table):
    '''
    Return nothing. Print info about the table.

    :param conn: sqlite conenction
    :param table: str
    :return: None
    '''
    print("Num entries: {}", get_num_rows(conn, table))


def get_num_rows(conn, table, sql=False):
    '''
    Returns the number of rows in the table.

    :param conn: sqlite conenction
    :param table: str
    :return: int
    '''
    c = conn.cursor()
    if sql:
        c.execute('SELECT rowid,* FROM {}'.format(table))
    else:
        c.execute('SELECT * FROM {}'.format(table))
    all_rows = c.fetchall()
    return len(all_rows)


def create_table(conn, table, cols):
    '''
    Return nothing. Create a table in the database.

    :param conn: sqlite3 connection
    :param table: str
    :param types: list of tuples indicating (name, type)
    :return: None

    Example usage:
    create_table('allpoems.db', 'poems', [('title', 'text'), ('poet', 'text')])

    Todo:
    catch errors in inputs.
    '''
    c = conn.cursor()

    cmd = "CREATE TABLE {} (".format(table)
    for entry in cols:
        cmd += "{} {},".format(entry[0], entry[1])
    cmd = cmd[:-1]  # remove last comma
    cmd += ")"

    c.execute(cmd)
    conn.commit()

    return None


def insert_vals(conn, table, vals, sql=False):
    '''
    Return nothing. Insert vals into table.

    :param conn: sqlite3 connection
    :param table: str
    :param vals: list
    :return: None
    '''
    c = conn.cursor()
    if sql:
        cmd = "INSERT INTO {} VALUES (null,".format(table)
    else:
        cmd = "INSERT INTO {} VALUES (".format("poetry (title, poet, url, poem)")
    for i in range(len(vals)):
        if sql:
            cmd += "?,"
        else:
            cmd += "%s,"
    cmd = cmd[:-1]  # remove last comma
    cmd += ")"

    c.execute(cmd, vals)
    conn.commit()

    return None


def check_for_poem(conn, table, poet, title, sql=False):
    '''
    Return True if the poem already exists in the database.

    :param conn: sqlite3 connection
    :param table: str
    :param poet: str
    :param title: str
    :return: boolean
    '''
    c = conn.cursor()
    if sql:
        cmd = "SELECT * FROM {} WHERE poet=? AND title=?".format(table)
    else:
        cmd = "SELECT * FROM {} WHERE poet=%s AND title=%s".format(table)
    c.execute(cmd, (poet, title))

    if len(c.fetchall()) == 0:
        return False
    return True


def get_values(conn, table, col, sql=False):
    '''
    Return list of values from col.

    :param conn: sqlite connection
    :param table: str
    :param col: str
    :return: list
    '''
    values = []

    if sql:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
    else:
        c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    c.execute('SELECT * FROM {}'.format(table))
    all_rows = c.fetchall()
    for row in sorted(all_rows):
        val = row[col]
        values.append(val)

    return values
