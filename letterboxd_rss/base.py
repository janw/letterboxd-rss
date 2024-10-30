from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor, wait
from typing import TYPE_CHECKING, Dict, List, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag

from letterboxd_rss.feed import create_feed
from letterboxd_rss.parsing import parse_page
from letterboxd_rss.session import session
from letterboxd_rss.utils import make_watchlist_url

if TYPE_CHECKING:
    from feedgen.feed import FeedEntry


def process(
    letterboxd_url: str,
    output_file: str,
    max_length: int,
) -> None:
    page_title = ""
    watchlist_url = make_watchlist_url(letterboxd_url)
    next_url: Optional[str] = watchlist_url + "page/1/"
    remaining_count = max_length
    with ThreadPoolExecutor(max_workers=4) as pool:
        future_to_url: Dict[Future[FeedEntry], str] = {}

        while next_url and remaining_count > 0:
            r = session.get_and_raise(next_url)
            soup = BeautifulSoup(r.text, "html.parser")

            next_url, _futures = parse_page(soup, max_movies=remaining_count, pool=pool)
            future_to_url.update(_futures)
            remaining_count -= len(_futures)

    entries: List[FeedEntry] = []
    for future in wait(future_to_url).done:
        url = future_to_url[future]
        try:
            entry = future.result()
        except Exception as exc:
            print("%r generated an exception: %s" % (url, exc))
        else:
            entries.append(entry)

    watchlist_title = soup.find("meta", attrs={"property": "og:title"})
    page_title = watchlist_title.attrs["content"] if isinstance(watchlist_title, Tag) else "The Dude's Watchlist"

    if entries:
        create_feed(
            entries,
            page_title=page_title,
            watchlist_url=watchlist_url,
            output_file=output_file,
        )
