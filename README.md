# Letterboxd RSS

<!-- markdownlint-disable MD033 MD013 -->
<div align="center">

[![version](https://img.shields.io/pypi/v/letterboxd-rss.svg)](https://pypi.org/project/letterboxd-rss/)
[![python](https://img.shields.io/pypi/pyversions/letterboxd-rss.svg)](https://pypi.org/project/letterboxd-rss/)
[![downloads](https://img.shields.io/pypi/dm/letterboxd-rss)](https://pypi.org/project/letterboxd-rss/)

<!-- [![Docker Build](https://github.com/janw/letterboxd-rss/actions/workflows/docker-build.yaml/badge.svg)](https://ghcr.io/janw/letterboxd-rss) -->
<!-- [![Tests](https://github.com/janw/letterboxd-rss/actions/workflows/tests.yaml/badge.svg)](https://github.com/janw/letterboxd-rss/actions/workflows/tests.yaml?query=branch%3Amain) -->
[![pre-commit.ci](https://results.pre-commit.ci/badge/github/janw/letterboxd-rss/main.svg)](https://results.pre-commit.ci/latest/github/janw/letterboxd-rss/main)

[![Maintainability](https://api.codeclimate.com/v1/badges/a3602f453bd063e6dcec/maintainability)](https://codeclimate.com/github/janw/letterboxd-rss/maintainability)
<!-- [![codecov](https://codecov.io/gh/janw/letterboxd-rss/branch/main/graph/badge.svg?token=G8WI2ZILRG)](https://codecov.io/gh/janw/letterboxd-rss) -->

[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://docs.astral.sh/ruff/)
[![poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/docs/)
[![pre-commit](https://img.shields.io/badge/-pre--commit-f8b424?logo=pre-commit&labelColor=grey)](https://github.com/pre-commit/pre-commit)

</div>

Convert your [Letterboxd] Watchlist to an RSS feed.

## Setup

Install via [pipx](https://pipx.pypa.io/stable/):

```bash
pipx install letterboxd-rss
```

## Usage

After installing, you may simply call letterboxd-rss from the command line:

```bash
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
