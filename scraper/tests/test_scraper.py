from scraper import scraper
from scraper.tests.text import text1, text2

from bs4 import BeautifulSoup
from urllib.request import urlopen

url1 = 'https://www.poetryfoundation.org/poems-and-poets/poems/detail/90734'
poet1 = 'Warsan Shire'
title1 = 'Backwards'

url2 = 'https://www.poetryfoundation.org/poems-and-poets/poems/detail/57956'
poet2 = 'Erika Meitner'
title2 = 'Staking a Claim'


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


def test_scrape_poem_page():
    pass
