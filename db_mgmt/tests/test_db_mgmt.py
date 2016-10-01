from db_mgmt import db_mgmt

import sqlite3
import pytest
import os


@pytest.fixture(scope="module")
def conn(request):
    conn = sqlite3.connect('temp/test.db')
    c = conn.cursor()
    c.execute("CREATE TABLE poetry (poet text, title text)")
    conn.commit()

    def fin():
        print ("teardown conn")
        conn.close()
        os.remove('temp/test.db')
    request.addfinalizer(fin)
    return conn  # provide the fixture value

def test_check_for_poem(conn):
    c = conn.cursor()
    check1 = db_mgmt.check_for_poem(conn, 'poetry', 'Poet', 'Title')
    assert check1 is False

    c.execute("INSERT INTO poetry VALUES (?,?)", ('Poet', 'Title'))

    check2 = db_mgmt.check_for_poem(conn, 'poetry', 'Poet', 'Title')
    assert check2 is True

    c.execute("INSERT INTO poetry VALUES (?,?)", ('Poet L. Name', 'Title is Title'))

    check2 = db_mgmt.check_for_poem(conn, 'poetry', 'Poet L. Name', 'Title is Title')
    assert check2 is True

def test_insert_vals(conn):
    db_mgmt.insert_vals(conn, 'poetry', ('poet name', 'title is'))
    check = db_mgmt.check_for_poem(conn, 'poetry', 'poet name', 'title is')
    assert check is True
