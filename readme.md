# Poetry Recommendation Engine

### VirtualEnv
Install all required packages in a virtaul environment:

`pip install -r requirements.txt`

### Tests
Run the tests using py.test within the the virtual environment (but not running the tests including the code in the virtual environment itself):

`python -m py.test --ignore=venv`

### Scrape Poems

Scraped poems are entered into a Postgres database in a table called `poetry`. Settings for the database must be set in a .env file.

Poems are scraped from poetryfoundation.org. Poem pages have urls like this:

`https://www.poetryfoundation.org/poems-and-poets/poems/detail/48761`

Not all poem pages have poems. Some poem pages have poems as images, not text, which is currently not supported. So when you scrape poems you need to specify the first and last number of the poem pages you want to attempt to collect poems from. All pages for which poems are added to the database are printed out in the console.

`python create_db.py --add-poems -s 48000 -e 48050`

### Run Analysis

???
