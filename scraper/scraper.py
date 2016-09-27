# based on https://github.com/eli8527/poetryfoundation-scraper/

from db_mgmt import db_mgmt

from bs4 import BeautifulSoup
from urllib.request import urlopen
import html


def get_poem_text(soup):
    '''
    Return text of poem.

    :param soup: BeautifulSoup object
    :return: str
    '''
    poem = ''
    poem_content = soup.find_all('div', {'class': 'poem'})
    for content in poem_content:
        for line in content.find_all('div'):
            text = html.parser.unescape(line.text).encode('utf8')
            out = text.decode('utf8').strip()
            poem += "{}\n".format(out)
    return poem


def get_poem_info(soup):
    '''
    Return (title, poet).

    :param soup: BeautifulSoup object
    :return: tuple
    '''
    title = soup.find("meta", property="og:title")["content"]
    poet = soup.find("meta", property="article:author")["content"]

    return (title, poet)


def scrape_poem_page(conn, table, url):
    '''
    Place poem info into database if it is not already there.

    :param url: list of bs4 contents
    :param table: str
    :return: None
    '''
    page = urlopen(url)
    soup = BeautifulSoup(page.read(), "lxml")
    title, poet = get_poem_info(soup)
    if (db_mgmt.check_for_poem(conn, table, poet, title)):
        text = get_poem_text(soup)
        db_mgmt.insert_vals(conn, table, (title, poet, url, text))
    return None


def scrape_website(base_url, function):
    '''
    Run through all pages and apply function.

    :param base_url: str
    :param function: function
    :return: None
    '''
    return None
