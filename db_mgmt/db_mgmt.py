"""Functions for inserting and retrieving data from a database."""
import dotenv
import sqlite3
import psycopg2
import psycopg2.extras
import os

from pony import orm

db = orm.Database()

class Poetry(db.Entity):
    title = orm.Required(str)
    poet = orm.Required(str)
    poem = orm.Required(str)
    url = orm.Optional(str)

    # could just add new things as numbers floats I don't know.
    # source = orm.Optional(str)

# TODO: function to add columns programmatically


class DatabaseManager(object):

    def __init__(self, database, user, host, password='', port='', create_tables=False):
        self.db = db
        self.db.bind('postgres', user=user, host=host,
            password=password, database=database, port=port)
        self.db.generate_mapping(create_tables=create_tables)

    @orm.db_session
    def print_random_poem(self):
        ''' lol not random '''
        p = orm.select(p for p in Poetry).first()
        print(p.title)
        print(p.poem)


    @orm.db_session
    def print_table_info(self):
        '''
        Return nothing. Print info about the table.

        :param table: str
        :return: None
        '''
        print("Num entries: {}".format(orm.count(p for p in Poetry)))


    @orm.db_session
    def add_poem(self, title, poet, url, poem):
        p = Poetry(title=title, poet=poet, url=url, poem=poem)
        orm.commit()

    @orm.db_session
    def get_poem(self, id='', title=''):
        '''
        Returns a dictionary representation of a poem, which must include the
        following keys (which map to strings, unless noted otherwise): title,
        url, poem, poet, id (maps to an integer).

        Must specify either an id or a title. If no poem is found, returns None.

        :param id: unique index into database for the poem
        :param title: title of the poem
        :return: dictionary or None
        '''
        poem = None
        if idx != '':
            poem = Poetry[id]
        elif title != '':
            poem = Poetry.get(title=title)

        if poem is None:
            return None
        return poem.to_dict()

        # If you don't want the other column values, (e.g. feature columns)
        # return this instead:

        # return {
        #     "id": poem.id,
        #     "title": poem.title,
        #     "url": poem.url,
        #     "poet": poem.poet,
        #     "poem": poem.poem
        # }


    @orm.db_session
    def update_poem(self, id='', title='', update_dict):
        '''
        Updates the poem based on id or title. For each key, value in update_dict,
        will set the database column which matches the key with the value.
        '''
        poem = None
        if id != '':
            poem = Poetry[id]
        elif title != '':
            poem = Poetry.get(title=title)

        if poem is None:
            raise RuntimeError("To update poem, must specify either an index or a title")

        poem.set(**update_dict)

