from db_mgmt import db_mgmt

import sqlite3
import pytest
import psycopg2
import testing.postgresql
import os
import warnings


@pytest.fixture(scope="module")
def conn(request):
    conn = sqlite3.connect('temp/test.db')
    c = conn.cursor()
    c.execute("CREATE TABLE poetry (id integer primary key, poet text, title text, url text, poem text)")
    conn.commit()

    def fin():
        print ("teardown conn")
        conn.close()
        os.remove('temp/test.db')
    request.addfinalizer(fin)
    return conn  # provide the fixture value



def test_check_for_poem(conn):
    c = conn.cursor()
    check1 = db_mgmt.check_for_poem(conn, 'poetry', 'Poet', 'Title', sql=True)
    assert check1 is False

    c.execute("INSERT INTO poetry VALUES (null, ?,?,?,?)", ('Poet', 'Title', 'none', 'none'))

    check2 = db_mgmt.check_for_poem(conn, 'poetry', 'Poet', 'Title', sql=True)
    assert check2 is True

    c.execute("INSERT INTO poetry VALUES (null, ?,?,?,?)", ('Poet L. Name', 'Title is Title', 'none', 'none'))

    check2 = db_mgmt.check_for_poem(conn, 'poetry', 'Poet L. Name', 'Title is Title', sql=True)
    assert check2 is True


def test_db_mgmt_postgres():
    with testing.postgresql.Postgresql() as postgresql:
        conn = psycopg2.connect(**postgresql.dsn())
        c = conn.cursor()
        c.execute("CREATE TABLE poetry (id serial primary key, title text, poet text, url text, poem text)")

        # test check_for_poem
        c.execute("INSERT INTO poetry (title, poet, url, poem) VALUES (%s,%s,%s,%s)", ('Title is Title', 'Poet L. Name', 'none', 'none'))
        check = db_mgmt.check_for_poem(conn, 'poetry', 'Poet L. Name', 'Title is Title')
        assert check is True

        # test insert_vals
        db_mgmt.insert_vals(conn, 'poetry', ('title is', 'poet name', 'none', 'none'))
        check = db_mgmt.check_for_poem(conn, 'poetry', 'poet name', 'title is')
        assert check is True

        # test get_num_rows
        num_rows = db_mgmt.get_num_rows(conn, 'poetry')
        assert num_rows == 2

        # test get_values
        db_mgmt.insert_vals(conn, 'poetry', ('title3', 'poet3', 'none', 'none'))
        db_mgmt.insert_vals(conn, 'poetry', ('title4', 'poet4', 'none', 'none'))
        db_mgmt.insert_vals(conn, 'poetry', ('title5', 'poet5', 'none', 'none'))
        poem_titles = db_mgmt.get_values(conn, 'poetry', 'title')
        assert ['Title is Title', 'title is', 'title3', 'title4', 'title5'] == poem_titles

        # test get_values after an udpated value
        c.execute("UPDATE poetry SET title=%s WHERE id=%s", ('title2', 2))
        poem_titles = db_mgmt.get_values(conn, 'poetry', 'title')
        assert ['Title is Title', 'title2', 'title3', 'title4', 'title5'] == poem_titles



def test_insert_vals(conn):
    db_mgmt.insert_vals(conn, 'poetry', ('poet name', 'title is', 'none', 'none'), sql=True)
    check = db_mgmt.check_for_poem(conn, 'poetry', 'poet name', 'title is', sql=True)
    assert check is True


def test_get_num_rows(conn):
    num_rows = db_mgmt.get_num_rows(conn, 'poetry', sql=True)
    assert num_rows == 3


def test_get_values(conn):
    warnings.warn("get_values no longer supports sql databases")
    assert True
    # poems = db_mgmt.get_values(conn, 'poetry', 'poem', sql=True)
    # assert len(poems) == 3
    # assert poems == ['none', 'none', 'none']

    # titles = db_mgmt.get_values(conn, 'poetry', 'title', sql=True)
    # assert titles == ['Title', 'Title is Title', 'title is']
