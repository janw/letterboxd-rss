# Letterboxd-RSS

Convert your [Letterboxd] Watchlist to an RSS feed.

## Installation

Install and update using [pip]:

```
pip install letterboxd-rss
```

## Usage

After installing, you may simply call letterboxd-rss from the command line:

```
$ letterboxd-rss -h

usage: letterboxd-rss [-h] [-o FEED_FILENAME] [-l FEED_LENGTH]
                      LETTERBOXD_PROFILE

positional arguments:
  LETTERBOXD_PROFILE    URL of your letterboxd profile

optional arguments:
  -h, --help            show this help message and exit
  -o FEED_FILENAME, --output FEED_FILENAME
                        Destination of the generated RSS feed (defaults to
                        ./feed.xml)
  -l FEED_LENGTH, --max-length FEED_LENGTH
                        Maximum number of watchlist items to keep in the feed
```


[Letterboxd]: https://letterboxd.com
[pip]: https://pip.pypa.io/en/stable/quickstart/
