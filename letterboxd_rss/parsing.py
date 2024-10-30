from __future__ import annotations

import re
from concurrent.futures import Future, ThreadPoolExecutor
from typing import TYPE_CHECKING, Dict, Optional, Tuple

from bs4 import BeautifulSoup
from feedgen.feed import FeedEntry

from letterboxd_rss.constants import BASE_URL
from letterboxd_rss.session import session

if TYPE_CHECKING:
    from concurrent.futures import Future, ThreadPoolExecutor


match_imdb = re.compile(r"^https?://www.imdb.com")
match_tmdb = re.compile(r"^https?://www.themoviedb.org")


def parse_page(
    soup: BeautifulSoup,
    max_movies: int,
    pool: ThreadPoolExecutor,
) -> Tuple[Optional[str], Dict[Future[FeedEntry], str]]:
    ul = soup.find("ul", attrs={"class": "poster-list"})

    next_url: Optional[str] = None
    t_next_link = soup.find("a", attrs={"class": "next"})
    if t_next_link:
        next_url = BASE_URL + t_next_link.attrs["href"]

    future_to_url: Dict[Future[FeedEntry], str] = {}
    for count, movie in enumerate(ul.find_all("li"), 1):
        movie_url = BASE_URL + "/film/" + movie.div.attrs["data-film-slug"]
        future_to_url[pool.submit(extract_metadata, movie_url)] = movie_url

        if count >= max_movies:
            next_url = None
            break

    return next_url, future_to_url


def extract_metadata(movie_url: str) -> Optional[FeedEntry]:
    movie_page = session.get_and_raise(movie_url)
    movie_soup = BeautifulSoup(movie_page.text, "html.parser")
    try:
        movie_title = movie_soup.find("meta", attrs={"property": "og:title"}).attrs["content"]
        print("Found", movie_title)
        movie_link = movie_soup.find("a", attrs={"href": [match_imdb, match_tmdb]}).attrs["href"]
        if movie_link.endswith("/maindetails"):
            movie_link = movie_link[:-11]
        movie_description = movie_soup.find("meta", attrs={"property": "og:description"})
        if movie_description is not None:
            movie_description = movie_description.text.strip()

        item = FeedEntry()
        item.title(movie_title)
        item.description(movie_description)
        item.link(href=movie_link, rel="alternate")
        item.guid(movie_link)
        return item

    except Exception as exc:
        print(f"Parsing failed on {movie_url}: {exc}")

    return None
