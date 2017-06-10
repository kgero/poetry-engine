import psycopg2
import dotenv

from scraper import scraper
from bs4 import BeautifulSoup
from urllib.request import urlopen


SCRAPER = False
DB = False
MATH = True

if SCRAPER:
    # found one at 40080

    i = 50000
    while i < 60000:
        i += 1
        url = "https://www.poetryfoundation.org/poems-and-poets/poems/detail/" + str(i)
        try:
            page = urlopen(url)
            soup = BeautifulSoup(page.read(), "lxml")
            text = scraper.get_poem_text(soup)
            if len(text) > 0:
                print(url)
        except:
            continue

if DB:
    dotenv.load()
    DATABASE = dotenv.get('DATABASE')
    USER = dotenv.get('DBUSER')
    HOST = dotenv.get('HOST')
    PASSWORD = dotenv.get('PASSWORD')
    cmd = "dbname='{}' user='{}' host='{}' password='{}'".format(DATABASE, USER, HOST, PASSWORD)
    print(cmd)
    conn = psycopg2.connect(cmd)


if MATH:
    x = 5000
    calc = (x * (x-1) / 2)
    print("Calc: {}".format(calc))

print("made it!")