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
    dbmdb = Path(args.dbmdb)
    destination = Path(args.destination[0])
    if not destination.is_dir():
        destination.mkdir(parents=True)
    if args.delete:
        for f in destination.iterdir():
            if f.is_file():
                f.unlink()
    for path_in in dbmdb.glob('*.md'):
        with path_in.open('r') as f_in:
            content = MD.convert(f_in.read())
        with (destination / ('%s.html' % path_in.stem)).open('w') as f_out:
            f_out.write(content)
