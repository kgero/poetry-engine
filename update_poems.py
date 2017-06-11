from db_mgmt.db_mgmt import DatabaseManager
from db_mgmt.db_mgmt import Poetry
from pony import orm
from scraper import pf_scraper

SCRAPING_TIME = 123123

@orm.db_session
def update_all_poems():
    for db_poem in orm.select(p for p in Poetry).order_by(Poetry.id)[529:1000]:
        try:
            poem_data = pf_scraper.scrape_poem_page(db_poem.url)
            db_poem.set(**poem_data)
            print("Updated poem {}:".format(db_poem.id))
            print(db_poem.title, " by ", db_poem.poet)
            orm.commit()
        except LookupError:
            print("Poem not found on page")
        except KeyboardInterrupt:
            print("Hey there, I see you want to stop.")
            return

if __name__ == "__main__":
    db_manager = DatabaseManager()
    update_all_poems()
