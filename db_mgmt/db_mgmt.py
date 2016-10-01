"""Functions for inserting and retrieving data from a database."""


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


def insert_vals(conn, table, vals):
    '''
    Return nothing. Insert vals into table.

    :param conn: sqlite3 connection
    :param table: str
    :param vals: list
    :return: None
    '''
    c = conn.cursor()
    cmd = "INSERT INTO {} VALUES (".format(table)
    for i in range(len(vals)):
        cmd += "?,"
    cmd = cmd[:-1]  # remove last comma
    cmd += ")"

    c.execute(cmd, vals)
    conn.commit()

    return None


def check_for_poem(conn, table, poet, title):
    '''
    Return True if the poem already exists in the database.

    :param conn: sqlite3 connection
    :param table: str
    :param poet: str
    :param title: str
    :return: boolean
    '''
    c = conn.cursor()
    cmd = "SELECT * FROM {} WHERE poet=? AND title=?".format(table)
    print(cmd)
    c.execute(cmd, (poet, title))

    if len(c.fetchall()) == 0:
        return False
    return True
