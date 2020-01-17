#!/usr/bin/env python3
import actions
import argparse
import sys

def parse_cmd_line():
    """ Print usage and process command line options. """

    parser = argparse.ArgumentParser(description="Lightweight Transactions Benchmark")

    parsers = parser.add_subparsers(title="Available actions")

    for Cls in actions.registry.values():
        subparser = parsers.add_parser(Cls.name, help=Cls.description)
        subparser.set_defaults(func=Cls().func)
        Cls.setup_argparse(subparser)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        sys.exit(parser.print_help())

    return args


if __name__ == "__main__":

    args = parse_cmd_line()

    args.func(args)
