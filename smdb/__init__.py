#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from subprocess import call

from jinja2 import Template
from markdown import Markdown

from mdb_settings import DBMDB, DIFFER, FILENAME_PATTERN, MD, META, parser_args
parser = ArgumentParser(description='Static MarkDown Blog')
parser_args(parser)
parser.add_argument('destination', nargs=1, type=str,
        help='Destination of the generated static files')

if __name__ == '__main__':
    args = parser.parse_args()
    destination = Path(args.destination[0])
    if not destination.is_dir():
        destination.mkdir(parents=True)
    if args.delete:
        for f in destination.iterdir():
            if f.is_file():
                f.unlink()


