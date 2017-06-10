from db_mgmt.db_mgmt import DatabaseManager
from db_mgmt.db_mgmt import Poetry
from pony import orm
from scraper import pf_scraper


SCRAPING_TIME = 123123

@orm.db_session
def update_all_poems():
    c = 0
    for db_poem in orm.select(p for p in Poetry)[:2]:
        try:
            poem_data = pf_scraper.scrape_poem_page(db_poem.url)
            db_poem.set(**poem_data)
            print("Updated poem:")
            print(db_poem.title, " by ", db_poem.poet)
            print("url was: ", db_poem.url)
        except LookupError:
            print("Poem not found on page")
        except:
            print("Url not found (!)", url)

if __name__ == "__main__":
    db_manager = DatabaseManager()
    update_all_poems()
