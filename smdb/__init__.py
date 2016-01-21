#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from subprocess import call
from os.path import dirname, expanduser

import jinja2
import yaml

from mdb_settings import MD, META, parser_args

DEFAULT_DEST = '/tmp/smdb'
DEFAULT_TEMP = Path(dirname(__file__)) / 'template.html'
DEFAULT_CONF = expanduser('~/.config/smdb.yml')

parser = ArgumentParser(description='Static MarkDown Blog')
parser_args(parser)
parser.add_argument('-s', '--sync', action='store_true', help="launch rsync")
parser.add_argument('-c', '--config', type=str, default=DEFAULT_CONF, help="Configuration file. (%s)" % DEFAULT_CONF)
parser.add_argument('destination', nargs='?', type=str, default=DEFAULT_DEST,
                    help='Destination of the generated static files. (%s)' % DEFAULT_DEST)
parser.add_argument('template', nargs='?', type=str, default=DEFAULT_TEMP,
                    help='Destination of the main template. (%s)' % DEFAULT_TEMP)


def main():
    args = parser.parse_args()
    dbmdb, destination, config, template = [Path(args.__dict__[k]) for k in [
        'dbmdb', 'destination', 'config', 'template']]
    with template.open('r') as template_file:
        jinja_template = jinja2.Template(template_file.read())
    with config.open('r') as config_file:
        yaml_config = yaml.load(config_file)
    for site, conf in yaml_config.items():
        path = destination / site
        if not path.is_dir():
            path.mkdir(parents=True)
        if args.delete:
            for f in path.iterdir():
                if f.is_file():
                    f.unlink()
        for path_in in dbmdb.glob('*.md'):
            context = conf.copy()
            context['current'] = path_in.stem
            with path_in.open('r') as input_file:
                context['content'] = MD.convert(input_file.read())
            for key, converter in META.items():
                if key in MD.Meta:
                    context[key] = converter(MD.Meta[key][0])
            if 'sites' not in MD.Meta or site in MD.Meta['sites'][0]:
                with (path / path_in.stem).open('w') as f_out:
                    f_out.write(jinja_template.render(**context))
        if args.sync:
            call(['rsync', '-avzP', str(path) + '/', conf['ssh']])
