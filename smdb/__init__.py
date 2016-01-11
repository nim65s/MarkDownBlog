#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from subprocess import call

from jinja2 import Template

from mdb_settings import MD, META, parser_args

parser = ArgumentParser(description='Static MarkDown Blog')
parser_args(parser)
parser.add_argument('destination', nargs='?', type=str, default='/tmp/smdb/',
        help='Destination of the generated static files. Default: /tmp/smdb/')

SITES_CONFIG = {
        'LAAS': {
            'title': 'Guilhem Saurel',
            'author': 'Guilhem Saurel',
            'links': [
                ('https://saurel.me', 'Blog'),
                ('https://twitter.com/nim65s', 'Twitter'),
                ('https://github.com/nim65s/', 'GitHub'),
                ],
            'pages': ['transHumUs'],
            'lang': 'fr',
            'url': 'http://homepages.laas.fr/gsaurel/',
            'ssh': 'gsaurel@homepages.laas.fr',
            },
        'n7': {
            'author': 'Guilhem Saurel',
            'title': 'Guilhem Saurel',
            'links': [
                ('https://saurel.me', 'Blog'),
                ('https://twitter.com/nim65s', 'Twitter'),
                ('https://github.com/nim65s/', 'GitHub'),
                ],
            'pages': ['transHumUs'],
            'lang': 'fr',
            'ssh': 'n7:www/',
            'url': 'http://bde.enseeiht.fr/~saurelg/',
            },
        }


if __name__ == '__main__':
    args = parser.parse_args()
    dbmdb = Path(args.dbmdb)
    destination = Path(args.destination)
    print('dbmdb: %s\ndesti: %s' % (dbmdb, destination))
    template = Template(Path('template.html').open().read())
    for site, conf in SITES_CONFIG.items():
        dest = destination / site
        print('dest:', dest)
        if not dest.is_dir():
            dest.mkdir(parents=True)
        if args.delete:
            for f in dest.iterdir():
                if f.is_file():
                    f.unlink()
        for path_in in dbmdb.glob('*.md'):
            context = conf.copy()
            context['current'] = path_in.stem
            with path_in.open('r') as f_in:
                context['content'] = MD.convert(f_in.read())
            if 'author' in MD.Meta:
                context['author'] = MD.Meta['author']
            if 'sites' not in MD.Meta or site in MD.Meta['sites']:
                with (dest / ('%s.html' % path_in.stem)).open('w') as f_out:
                    f_out.write(template.render(**context))
        # call(['rsync', '-avzP', str(dist) + '/', conf['ssh']])
