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


def get_poem_tags(soup):
    '''
    Return string of comma separated tags.

    :param soup: BeautifulSoup object
    :return: str
    '''
    tags = soup.find("meta", property="article:tag")["content"]
    return tags


def get_poem_copyright(soup):
    '''
    Return string of copyrighti information.

    I'm thinking later I can parse this for original publication
    and original publication date.

    :param soup: BeautifulSoup object
    :return: str
    '''
    user_content = soup.find_all('div', {'class': 'user-content-text user-content-text_understate user-content-text_subtle'})
    text = ""
    for tag in user_content:
        text += tag.get_text().strip() + " "
    text = text.replace('"', "'")
    text = text.replace('”', "'")
    text = re.sub('\s+', ' ', text).strip()
    return text


def scrape_poem_page(url):
    '''
    Return poem data as dictionary. Dictionary keys should match table columns.
    title, poet, url, poem, tags, copyright

    :param url: str
    :return: dict
    '''
    page = urlopen(url)
    soup = BeautifulSoup(page.read(), "lxml")
    poem = get_poem_text(soup)
    if len(poem) == 0:
        raise LookupError('No poem found on page. Sorry!')

    title, poet = get_poem_info(soup)
    copyright = get_poem_copyright(soup)
    tags = get_poem_tags(soup)

    return {
        'title': title,
        'poet': poet,
        'url': url,
        'poem': poem,
        'copyright': copyright,
        'tags': tags,
        'source': 'Poetry Foundation'
    }
