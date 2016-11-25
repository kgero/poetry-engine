# based on https://github.com/eli8527/poetryfoundation-scraper/

from db_mgmt import db_mgmt

from bs4 import BeautifulSoup
from urllib.request import urlopen
import html
import re


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
            out = out.replace('\xa0', ' ')
            poem += "{}\n".format(out)
    return poem


def get_poem_info(soup):
    '''
    Return (title, poet).

    :param soup: BeautifulSoup object
    :return: tuple
    '''
    title = soup.find("span", attrs={'class': 'hdg hdg_1'}).text
    poet = soup.find("meta", property="article:author")["content"]

    return (title, poet)


def scrape_poem_page(conn, table, url, sql=False):
    '''
    Place poem info into database if it has text and is not already there.

    Return True is poem is inserted.

    :param conn: sqlite connection
    :param table: str
    :param url: str
    :return: None
    '''
    try:
        page = urlopen(url)
    except:
        return False

    soup = BeautifulSoup(page.read(), "lxml")
    poem = get_poem_text(soup)
    if len(poem) == 0:
        return False

    title, poet = get_poem_info(soup)
    if db_mgmt.check_for_poem(conn, table, poet, title, sql=sql) is False:
        poem = get_poem_text(soup)

        print(title, poet, url)
        db_mgmt.insert_vals(conn, table, (title, poet, url, poem), sql=sql)
        return True
    return False


def scrape_website(conn, table, base_url, start_num, end_num, print_output=False, sql=False):
    '''
    Run through all pages and apply function.

    base_url: https://www.poetryfoundation.org/poems-and-poets/poems/detail/
    example_url: https://www.poetryfoundation.org/poems-and-poets/poems/detail/48160

    :param conn: slqlite connection
    :param table: str
    :param base_url: str
    :param start_num: int
    :param end_num: int
    :param print_output: bool
    :return: None
    '''
    i = start_num
    while i <= end_num:
        url = base_url + str(i)
        success = scrape_poem_page(conn, table, url, sql=sql)
        if success and print_output:
            print(url)
        i += 1

    return None
