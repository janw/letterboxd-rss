import sys
import argparse
from letterboxd_rss import process


def main(argv=None):
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
        help="Maximum number of watchlist items to keep in the feed",
    )
    args = parser.parse_args(argv)
    process(args)


main(sys.argv[1:])
