#!/usr/bin/env python3

from requests import session
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from configparser import ConfigParser
import re

c = ConfigParser()
c.read('config.ini')

feedlen = c['default'].getint('feed_length', 100)
watchlist_url = c['default'].get('watchlist_url', 'https://letterboxd.com/janwh/watchlist/')
output_file = c['default'].get('output_file', 'feed.xml')
base_url = 'https://letterboxd.com/'
page_title = 'The Dude\'s Watchlist'

s = session()
r = s.get(watchlist_url)

soup = BeautifulSoup(r.text, 'html.parser')


watchlist_title = soup.find('meta', attrs={'property': 'og:title'})
if watchlist_title is not None:
    page_title = watchlist_title.attrs['content']

feed = FeedGenerator()
feed.title(page_title)
feed.id(watchlist_url)
feed.link(href=watchlist_url, rel='alternate')
feed.description(page_title + ' from Letterboxd')

posters = soup.findAll('div', attrs={'class', 'poster'})
match_imdb = re.compile('^http://www.imdb.com')

if len(posters) == 0:
    return
elif len(posters) > feedlen:
    posters = posters[:feedlen]

print('Adding %i movies ...' % len(posters))

for movie in posters:

    movie_page = s.get(base_url+movie.attrs['data-film-slug'])
    movie_soup = BeautifulSoup(movie_page.text, 'html.parser')

    movie_title = movie_soup.find('meta', attrs={'property': 'og:title'}).attrs['content']
    movie_link = movie_soup.find('a', attrs={'href': match_imdb}).attrs['href']
    movie_link = movie_link[:-11]
    movie_description = movie_soup.find('div', attrs={'class': 'truncate'})
    movie_description = movie_description.text.strip()

    item = feed.add_item()
    item.title(movie_title)
    item.description(movie_description)
    item.link(href=movie_link, rel='alternate')
    item.guid(movie_link)

    print('Added movie', movie_title)

feed.rss_file(output_file)
