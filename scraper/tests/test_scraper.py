from scraper import scraper
from scraper.tests.text import text1, text2

from bs4 import BeautifulSoup
from urllib.request import urlopen

import pytest

url1 = 'https://www.poetryfoundation.org/poems-and-poets/poems/detail/90734'
poet1 = 'Warsan Shire'
title1 = 'Backwards'
tags1 = 'Living,Health & Illness,Life Choices,The Body,Youth,\
Relationships,Family & Ancestors,Home Life,Men & Women,Health & \
Illness,Life Choices,The Body,Youth,Family & Ancestors,Home Life,\
Men & Women,Meters,Free Verse,Free Verse'
copyright1 = "Warsan Shire, 'Backwards.' Copyright © 2014 by Warsan Shire."

url2 = 'https://www.poetryfoundation.org/poems-and-poets/poems/detail/57956'
poet2 = 'Erika Meitner'
title2 = 'Staking a Claim'
tags2 = 'Love,Desire,Arts & Sciences,Poetry & Poets,Desire,Poetry & Poets,\
Nostalgia,Passion,Life,Love,Youth'
copyright2 = "Erika Meitner, 'Staking a Claim' from Copia. Copyright © 2014 by \
Erika Meitner. Reprinted by permission of BOA Editions, Ltd. Source: Copia \
(BOA Editions Ltd., 2014)"

url404 = 'https://www.poetryfoundation.org/poetrymagazine/poems/detail/61596'
url_image = 'https://www.poetryfoundation.org/poetrymagazine/poems/detail/21596'

base_url = 'https://www.poetryfoundation.org/poems-and-poets/poems/detail/'

# failed poem title: This Can&rsquo;t Be

@pytest.fixture(scope="module")
def soups(request):
    page = urlopen(url1)
    soup1 = BeautifulSoup(page.read(), "lxml")

    page = urlopen(url2)
    soup2 = BeautifulSoup(page.read(), "lxml")

    return (soup1, soup2)


def test_get_poems(soups):
    soup = soups[0]
    title, poet = scraper.get_poem_info(soup)
    text = scraper.get_poem_text(soup)
    assert text1 == text
    assert title1 == title
    assert poet1 == poet

    soup = soups[1]
    title, poet = scraper.get_poem_info(soup)
    text = scraper.get_poem_text(soup)
    assert text2 == text
    assert title2 == title
    assert poet2 == poet


def test_get_poem_tags(soups):
    soup = soups[0]
    tags = scraper.get_poem_tags(soup)
    assert tags1 == tags

    soup = soups[1]
    tags = scraper.get_poem_tags(soup)
    assert tags2 == tags


def test_get_poem_copyright(soups):
    soup = soups[0]
    copyright = scraper.get_poem_copyright(soup)
    assert copyright1 == copyright

    soup = soups[1]
    copyright = scraper.get_poem_copyright(soup)
    assert copyright2 == copyright
