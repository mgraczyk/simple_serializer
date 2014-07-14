#!/usr/bin/python3

import argparse

from elftools.elf.elffile import ELFFile

def process_file(filename):
    print('Processing file:', filename)
    with open(filename, 'rb') as f:
        elffile = ELFFile(f)

        if not elffile.has_dwarf_info():
            print('  file has no DWARF info')
            return

        # get_dwarf_info returns a DWARFInfo context object, which is the
        # starting point for all DWARF-based processing in pyelftools.
        dwarfinfo = elffile.get_dwarf_info()

        for CU in dwarfinfo.iter_CUs():
            # DWARFInfo allows to iterate over the compile units contained in
            # the .debug_info section. CU is a CompileUnit object, with some
            # computed attributes (such as its offset in the section) and
            # a header which conforms to the DWARF standard. The access to
            # header elements is, as usual, via item-lookup.
            print('  Found a compile unit at offset %s, length %s' % (
                CU.cu_offset, CU['unit_length']))

            # Start with the top DIE, the root for this CU's DIE tree
            top_DIE = CU.get_top_DIE()
            print('    Top DIE with tag=%s' % top_DIE.tag)

            # We're interested in the filename...
            print('    name=%s' % top_DIE.get_full_path())

            # Display DIEs recursively starting with top_DIE
            die_info_rec(top_DIE)


def die_info_rec(die, indent_level='    '):
    """ A recursive function for showing information about a DIE and its
        children.
    """
    print(indent_level + 'DIE tag={} at {} -> {}\n'.format(die.tag, die.offset, str(die.attributes)))
    child_indent = indent_level + '  '
    for child in die.iter_children():
        die_info_rec(child, child_indent)

def get_arg_parser():
    argParser = argparse.ArgumentParser(description='Generates serialization functions for data structures inside an elf file.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argParser.add_argument('elf_file', help="Object file from which to read symbols")
    argParser.add_argument('out_file', type=str, default="/dev/stdout",
            help="Path where the output header will be written")

    return argParser

def main():
    args = get_arg_parser().parse_args()
    process_file(args.elf_file)

if __name__ == "__main__":
    main()
