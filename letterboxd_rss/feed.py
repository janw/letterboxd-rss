from __future__ import annotations

from typing import List

from feedgen.feed import FeedEntry, FeedGenerator


def create_feed(entries: List[FeedEntry], page_title: str, watchlist_url: str, output_file: str) -> None:
    feed = FeedGenerator()
    feed.title(page_title)
    feed.id(watchlist_url)
    feed.link(href=watchlist_url, rel="alternate")
    feed.description(page_title + " from Letterboxd")
    for entry in entries:
        feed.add_entry(entry)

    print(f"Writing feed to {output_file}")
    feed.rss_file(output_file)
