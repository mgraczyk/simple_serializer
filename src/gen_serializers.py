#!/usr/bin/python3

import argparse

def get_arg_parser():
    argParser = argparse.ArgumentParser(description='Generates serialization functions for data structures inside an elf file.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argParser.add_argument('elf_file', nargs=1, help="Object file from which to read symbols")
    argParser.add_argument('out_file', nargs=1, default="/dev/stdout",
            help="Path where the output header will be written")

    return argParser

def main():
    args = get_arg_parser().parse_args()

if __name__ == "__main__":
    main()
