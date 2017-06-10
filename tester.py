
from scraper import scraper
from bs4 import BeautifulSoup
from urllib.request import urlopen


page = urlopen("https://www.poetryfoundation.org/poems-and-poets/poems/detail/90734")
soup = BeautifulSoup(page.read(), "lxml")
scraper.get_poem_copyright(soup)