# Poetry Recommendation Engine

## Set-up

poetry-engine runs on python 3. Get with it!

### VirtualEnv

Install all required packages in a virtual environment (a python 3 virtual env!):

`pip install -r requirements.txt`

### Tests

Run the tests using py.test within the the virtual environment. (The last tags ensures we don't run the virtualenv tests, which are slow, not ours, and don't all pass):

`python -m py.test --ignore=venv`

To run a single file of tests add the test filename at the end:

`python -m py.test --ignore=venv features/tests/test_vocabulary_features.py`

### Scrape Poems

Scraped poems are entered into a Postgres database in a table called `poetry`. Settings for the database must be set in a .env file.

Poems are scraped from poetryfoundation.org. Poem pages have urls like this:

`https://www.poetryfoundation.org/poems-and-poets/poems/detail/48761`

Not all poem pages have poems. Some poem pages have poems as images, not text, which is currently not supported. So when you scrape poems you need to specify the first and last number of the poem pages you want to attempt to collect poems from. All pages for which poems are added to the database are printed out in the console.

`python create_db.py --add-poems -s 48000 -e 48050`

### Extract Features

???

### Find Nearest Neighbors

Find the 'nearest neighbor' for each poems by calculating the distance between all other poems and selecting one with the lowest distance. Distance is simply the sum of the differences squared for all features. (Alternatively you can select a subset of features to use.) Features are first normalized before the difference is calculated such that all features give the same weighting.

The script will store a pickle of the results dictionary to `temp/nearest_neighbor.p` such that the results do not need to be re-run every time. Include the `-r` flag if you want to force a re-run.

`python nearest_neighbor.py`