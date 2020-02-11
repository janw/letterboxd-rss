import re

from requests import session
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

match_imdb = re.compile(r"^https?://www.imdb.com")
match_tmdb = re.compile(r"^https?://www.themoviedb.org")

base_url = "https://letterboxd.com/"

MATCH_TOTAL_MOVIES = re.compile(r"to see (\d+)")
s = session()


def process(args):

    watchlist_url = args.letterboxd_url.rstrip("/")
    if not watchlist_url.startswith("https://"):
        watchlist_url = f"{base_url}{watchlist_url}"
    if not watchlist_url.endswith("watchlist"):
        watchlist_url += "/watchlist"
    watchlist_url += "/"

    feedlen = args.max_length
    output_file = args.output
    page_title = "The Dude's Watchlist"

    feed = FeedGenerator()
    feed.title(page_title)
    feed.id(watchlist_url)
    feed.link(href=watchlist_url, rel="alternate")
    feed.description(page_title + " from Letterboxd")

    # Get first page, gather general data
    r = s.get(watchlist_url)
    soup = BeautifulSoup(r.text, "html.parser")

    watchlist_title = soup.find("meta", attrs={"property": "og:title"})
    page_title = watchlist_title.attrs["content"]

    m = soup.find(text=MATCH_TOTAL_MOVIES)
    if len(m) > 0:
        total_movies = MATCH_TOTAL_MOVIES.search(m).group(1)
        total_movies = int(total_movies)
        print(f"Found a total of {total_movies} movies")

    last_page = soup.find_all("li", attrs={"class": "paginate-page"})[-1].text
    last_page = int(last_page)

    movies_added = 0
    for page in range(1, last_page):
        if page > 1:
            r = s.get(watchlist_url + "/page/%i/" % page)
            soup = BeautifulSoup(r.text, "html.parser")
            print()

        ul = soup.find("ul", attrs={"class": "poster-list"})
        movies = ul.find_all("li")
        movies_on_page = len(movies)

        print(f"Gathering on page {page} (contains {movies_on_page} movies)\n")

        for movie in movies:
            added = extract_metadata(movie, feed)

            # Update total counter
            movies_added += added
            if feedlen > 0 and movies_added >= feedlen:
                print("\nReached desired maximum feed length")
                break

        if feedlen > 0 and movies_added >= feedlen:
            break

    if movies_added > 0:
        print(f"Writing feed to {output_file}")
        feed.rss_file(output_file)


def extract_metadata(movie, feed):
    movie_slug = movie.div.attrs["data-film-slug"]
    movie_page = s.get(base_url + movie_slug)
    movie_soup = BeautifulSoup(movie_page.text, "html.parser")

    try:
        movie_title = movie_soup.find("meta", attrs={"property": "og:title"}).attrs[
            "content"
        ]
        print("Adding", movie_title)
        movie_link = movie_soup.find(
            "a", attrs={"href": [match_imdb, match_tmdb]}
        ).attrs["href"]
        if movie_link.endswith("/maindetails"):
            movie_link = movie_link[:-11]
        movie_description = movie_soup.find(
            "meta", attrs={"property": "og:description"}
        )
        if movie_description is not None:
            movie_description = movie_description.text.strip()

        item = feed.add_item()
        item.title(movie_title)
        item.description(movie_description)
        item.link(href=movie_link, rel="alternate")
        item.guid(movie_link)

        return 1
    except Exception:
        print("Parsing failed on", base_url + movie_slug)

    return 0
