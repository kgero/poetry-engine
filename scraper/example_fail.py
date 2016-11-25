from bs4 import BeautifulSoup
from urllib.request import urlopen

poem_page = urlopen("https://www.poetryfoundation.org/poems-and-poets/poems/detail/57956")
poem_soup = BeautifulSoup(poem_page.read(), "html5lib")
print(poem_soup)