#!/usr/bin/env python3

"""Parse src treatments."""

import argparse
import sys
import textwrap
from copy import deepcopy

import src.pylib.brazil_util as b_util
from src.matchers.pipeline import Pipeline
from src.readers.brazil_reader import brazil_reader
from src.writers.csv_writer import csv_writer
from src.writers.data_writer import biluo_writer, iob_writer, ner_writer
from src.writers.html_writer import html_writer


def get_brazil_families(args):
    """Handle Brazil Flora extractions"""
    families = {k: v for k, v in b_util.get_families().items() if v['count']}

    if args.list_families:
        b_util.print_families(families)
        sys.exit()

    family_set = {f.capitalize() for f in args.family}

    families = {k: v for k, v in families.items() if k in family_set}

    return families


def main(args):
    """Perform actions based on the arguments."""
    pipeline = Pipeline()
    families = get_brazil_families(args)

    rows = brazil_reader(args, families)

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

    if args.flora_id:
        args.flora_id = [int(i) for i in args.flora_id]
    else:
        args.flora_id = [1]

    if not (args.csv_file or args.html_file or args.ner_file or args.iob_file
            or args.biluo_file):
        setattr(args, 'csv_file', sys.stdout)

    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)
