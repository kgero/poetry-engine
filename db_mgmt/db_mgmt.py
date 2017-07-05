"""Functions for inserting and retrieving data from a database."""
import dotenv

from pony import orm

db = orm.Database()

class Poetry(db.Entity):
    title = orm.Required(str)
    poet = orm.Required(str)
    poem = orm.Required(str)
    url = orm.Optional(str)
    tags = orm.Optional(str)
    copyright = orm.Optional(str)
    source = orm.Optional(str)

    close_poem = orm.Optional(int)
    top_topic = orm.Optional(int)

    # size features
    num_lines = orm.Optional(int)
    num_words = orm.Optional(int)
    word_size = orm.Optional(float)
    width_in_char = orm.Optional(float)


def _get_params_from_dotenv():
    dotenv.load("../.env")
    return {
       'database': dotenv.get('DATABASE'),
       'user': dotenv.get('DBUSER'),
       'host': dotenv.get('HOST'),
       'password': dotenv.get('PASSWORD')
    }

    # could just add new things as numbers floats I don't know.
    # source = orm.Optional(str)

# TODO: function to add columns programmatically


class DatabaseManager(object):

    def __init__(self, database='', user='', host='', password='', port='', create_tables=False):
        self.db = db

        if database == '':
            self.db.bind('postgres', **_get_params_from_dotenv())
        else:
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
    def count_rows(self):
        return orm.count(p for p in Poetry)

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
        '''
        Adds a poem to the database if a poem with the same title and
        poet does not already exist.

        :return: True if poem is added, False if it is already present.
        '''
        # TODO: update this to check the text of the poem.
        if Poetry.get(poet=poet, title=title) is not None:
            return False

        p = Poetry(title=title, poet=poet, url=url, poem=poem)
        orm.commit()
        return True

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
        if id != '':
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
    def update_poem(self, id='', title='', update_dict={}):
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
