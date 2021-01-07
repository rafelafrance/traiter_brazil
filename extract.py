#!/usr/bin/env python3

"""Parse src treatments."""

import argparse
import json
import sys
import textwrap
from copy import deepcopy
from datetime import datetime

from src.matchers.pipeline import Pipeline
from src.pylib.consts import BRAZIL_DIR, BRAZIL_FAMILIES
from src.readers.brazil import brazil
from src.writers.csv_ import csv_writer
from src.writers.data import biluo_writer, iob_writer, ner_writer
from src.writers.html_ import html_writer


def main(args):
    """Perform actions based on the arguments."""
    pipeline = Pipeline()
    families = get_brazil_families(args)

    rows = brazil(args, families)

    for row in rows:
        row['doc'] = pipeline.nlp(row['text'])
        row['traits'] = pipeline.trait_list(row['doc'])

    if args.csv_file:
        copied = deepcopy(rows)
        csv_writer(args, copied)

    if args.html_file:
        copied = deepcopy(rows)
        html_writer(args, copied)

    if args.ner_file:
        copied = deepcopy(rows)
        ner_writer(args, copied)

    if args.iob_file:
        copied = deepcopy(rows)
        iob_writer(args, copied)

    if args.biluo_file:
        copied = deepcopy(rows)
        biluo_writer(args, copied)


def get_brazil_families(args):
    """Handle Brazil Flora extractions"""
    families = {k: v for k, v in get_families().items() if v['count']}

    if args.list_families:
        print_families(families)
        sys.exit()

    family_set = {f.capitalize() for f in args.family}

    families = {k: v for k, v in families.items() if k in family_set}

    return families


def get_families():
    """Get a list of all families in the Brazil catalog."""
    with open(BRAZIL_FAMILIES) as in_file:
        all_families = json.load(in_file)

    all_families = [f for f in all_families['result'] if f]

    families = {}

    for family in all_families:
        row = {'family': family, 'created': '', 'modified': '', 'count': 0}

        path = BRAZIL_DIR / family

        if path.exists():
            row['count'] = len(list(path.glob('*.html')))
            if row['count']:
                stat = path.stat()
                row['created'] = datetime.fromtimestamp(
                    stat.st_ctime).strftime('%Y-%m-%d %H:%M')
                row['modified'] = datetime.fromtimestamp(
                    stat.st_mtime).strftime('%Y-%m-%d %H:%M')

        families[family] = row

    return families


def print_families(families):
    """Display a list of all families."""
    template = '{:<20} {:<20} {:<20} {:>8}'

    print(template.format(
        'Family',
        'Directory Created',
        'Directory Modified',
        'Treatments'))

    for family in families.values():
        print(template.format(
            family['family'],
            family['created'],
            family['modified'],
            family['count'] if family['count'] else ''))


def parse_args():
    """Process command-line arguments."""
    description = """Parse data from flora website."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description),
        fromfile_prefix_chars='@')

    arg_parser.add_argument(
        '--family', '-f', action='append',
        help="""Which family to extract.""")

    arg_parser.add_argument(
        '--genus', '-g', action='append',
        help="""Which genus to extract with in the family. Default is
            to select all genera. Although this is designed for selecting
            genera this is really just a filter on the taxa names so you
            can put in anything that matches a taxon name.""")

    arg_parser.add_argument(
        '--html-file', '-H', type=argparse.FileType('w'),
        help="""Output the results to this HTML file.""")

    arg_parser.add_argument(
        '--csv-file', '-C', type=argparse.FileType('w'),
        help="""Output the results to this CSV file.""")

    arg_parser.add_argument(
        '--ner-file', '-N', type=argparse.FileType('a'),
        help="""Append formatted NER training data to this file.""")

    arg_parser.add_argument(
        '--iob-file', '-I', type=argparse.FileType('a'),
        help="""Append formatted training data in IOB format
            to this file.""")

    arg_parser.add_argument(
        '--biluo-file', '-B', type=argparse.FileType('a'),
        help="""Append formatted training data in BILUO format
            to this file.""")

    arg_parser.add_argument(
        '--list-families', '-l', action='store_true',
        help="""List families available to extract and exit.""")

    args = arg_parser.parse_args()

    if args.family:
        args.family = [f.lower() for f in args.family]
    else:
        args.family = []

    if not (args.csv_file or args.html_file or args.ner_file or args.iob_file
            or args.biluo_file):
        setattr(args, 'csv_file', sys.stdout)

    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)
