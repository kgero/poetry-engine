from db_mgmt.db_mgmt import DatabaseManager
from db_mgmt.db_mgmt import Poetry
from pony import orm
from scraper import scraper


SCRAPING_TIME = 123123

@orm.db_session
def update_all_poems():
	c = 0
	for db_poem in orm.select(p for p in Poetry):
		try:
		    poem_data = scraper.scrape_poem_page(db_poem.url)
		    db_poem.set(**poem_data)
		except LookupError:
			print("Poem not found on page")
	    except:
	    	print("Url not found (!)", url)

if __name__ == "__main__":
    db_manager = DatabaseManager()
    update_all_poems()
