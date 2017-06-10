from db_mgmt.db_mgmt import Poetry, DatabaseManager

import sqlite3
import pytest
import psycopg2
import testing.postgresql
import os
import warnings

from pony import orm


@pytest.fixture(scope="module")
def db_manager(request):
    postgresql = testing.postgresql.Postgresql()
    db_manager = DatabaseManager(create_tables=True, **postgresql.dsn())

    def fin():
        postgresql.stop()
    request.addfinalizer(fin)

    return db_manager


def test_add_poem(db_manager):

    # should return True
    assert db_manager.add_poem("my_poem", "poet name", "url thing", "textextext")
    assert db_manager.count_rows() == 1

    assert not db_manager.add_poem(
        "my_poem", "poet name", "different url", "textextext")
    assert db_manager.count_rows() == 1

    assert db_manager.add_poem(
        "different_poem", "poet name", "url thing2", "lorem ipsum")
    assert db_manager.count_rows() == 2

    with orm.db_session:
        p = Poetry.get(title="my_poem")

        assert p is not None
        assert p.poet == "poet name"
        assert p.poem == "textextext"
