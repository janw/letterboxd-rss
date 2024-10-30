from __future__ import annotations

from letterboxd_rss.constants import BASE_URL


def make_watchlist_url(val: str) -> str:
    url = val.rstrip("/")
    if not url.startswith("https://"):
        url = f"{BASE_URL}/{url}"
    if not url.endswith("watchlist"):
        url += "/watchlist"
    return url + "/"
