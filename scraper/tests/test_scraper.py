from scraper import scraper
from scraper.tests.text import text1, text2

from db_mgmt import db_mgmt

from bs4 import BeautifulSoup
from urllib.request import urlopen

import sqlite3
import pytest
import os

url1 = 'https://www.poetryfoundation.org/poems-and-poets/poems/detail/90734'
poet1 = 'Warsan Shire'
title1 = 'Backwards'

url2 = 'https://www.poetryfoundation.org/poems-and-poets/poems/detail/57956'
poet2 = 'Erika Meitner'
title2 = 'Staking a Claim'

url404 = 'https://www.poetryfoundation.org/poetrymagazine/poems/detail/61596'
url_image = 'https://www.poetryfoundation.org/poetrymagazine/poems/detail/21596'

base_url = 'https://www.poetryfoundation.org/poems-and-poets/poems/detail/'


@pytest.fixture(scope="module")
def conn(request):
    conn = sqlite3.connect('temp/test.db')
    c = conn.cursor()
    c.execute("CREATE TABLE poetry (title text, poet text, url text, poem text)")
    conn.commit()

    def fin():
        print ("teardown conn")
        conn.close()
        os.remove('temp/test.db')

    request.addfinalizer(fin)
    return conn  # provide the fixture value


def test_get_poems():
    page = urlopen(url1)
    soup = BeautifulSoup(page.read(), "lxml")
    title, poet = scraper.get_poem_info(soup)
    text = scraper.get_poem_text(soup)
    assert text1 == text
    assert title1 == title
    assert poet1 == poet

    page = urlopen(url2)
    soup = BeautifulSoup(page.read(), "lxml")
    title, poet = scraper.get_poem_info(soup)
    text = scraper.get_poem_text(soup)
    assert text2 == text
    assert title2 == title
    assert poet2 == poet


def test_scrape_poem_page(conn):

    # test pome 1
    inserted = scraper.scrape_poem_page(conn, 'poetry', url1)
    assert inserted is True

    check = db_mgmt.check_for_poem(conn, 'poetry', poet1, title1)
    assert check is True

    inserted = scraper.scrape_poem_page(conn, 'poetry', url1)
    assert inserted is False

    # test that poems of 0 length (i.e. image poems) are not inserted
    inserted = scraper.scrape_poem_page(conn, 'poetry', url_image)
    assert inserted is False

    # test that urls that produce 404 are not inserted
    inserted = scraper.scrape_poem_page(conn, 'poetry', url404)
    assert inserted is False


def test_scrape_website(conn):
    # test on a small num of nums
    scraper.scrape_website(conn, 'poetry', base_url, 48760, 48761)

    check = db_mgmt.check_for_poem(conn, 'poetry', 'June Jordan', 'Letter to the Local Police')
    assert check is True

    check = db_mgmt.check_for_poem(conn, 'poetry', 'June Jordan', 'On the Loss of Energy (and Other Things)')
    assert check is True
