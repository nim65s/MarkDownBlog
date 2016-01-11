from datetime import datetime
from difflib import Differ
from markdown import Markdown
from pathlib import Path


__all__ = ['DBMDB', 'DIFFER', 'FILENAME_PATTERN', 'MD', 'META', 'parser_args']


DBMDB = Path('.')
if (DBMDB / 'dbmdb').is_dir():
    DBMDB /= 'dbmdb'

DIFFER = Differ()

FILENAME_PATTERN = ['%s', '%s.md', '%s.markdown']

MD = Markdown(output_format='html5', extensions=[
    'markdown.extensions.codehilite',
    'markdown.extensions.meta',
    'markdown.extensions.nl2br',
    'markdown.extensions.sane_lists',
    ])

ident = lambda x: x

META = {
        'title': ident,
        'date': lambda x: datetime.strptime(x, '%Y-%m-%d').date(),
        'is_visible': lambda x: bool(int(x)),
        'author': ident,
        'template': ident,
        }

def parser_args(parser, dbmdb=DBMDB):
    parser.add_argument('dbmdb', nargs='?', type=str, default=str(dbmdb),
            help="""DataBase for MarkDownBlog: path to the folder of articles in
            markdown. Default: %s""" % dbmdb)
    parser.add_argument('-d', '--delete', action='store_true',
            help="Delete other entries")