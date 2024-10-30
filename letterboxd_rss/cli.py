from __future__ import annotations

import argparse
from typing import List, Optional

from letterboxd_rss.base import process


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "letterboxd_url",
        metavar="LETTERBOXD_PROFILE",
        help="URL of your letterboxd profile",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="FEED_FILENAME",
        default="./feed.xml",
        help="Destination of the generated RSS feed (defaults to ./feed.xml)",
    )
    parser.add_argument(
        "-l",
        "--max-length",
        metavar="FEED_LENGTH",
        default=20,
        type=int,
        help="Maximum number of watchlist items to keep in the feed",
    )
    args = parser.parse_args(argv)
    process(
        letterboxd_url=args.letterboxd_url,
        output_file=args.output,
        max_length=args.max_length,
    )
