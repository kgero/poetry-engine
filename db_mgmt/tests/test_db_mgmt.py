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

    db_manager.add_poem("my_poem", "poet name", "url thing", "textextext")

    with orm.db_session:
        p = Poetry.get(title="my_poem")
        p2 = Poetry.get(title="conspicuously_absent")

        assert p is not None
        assert p.poet == "poet name"
        assert p2 is None
