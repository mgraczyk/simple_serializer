#!/usr/bin/python3

import argparse
from collections import namedtuple

from elftools.elf.elffile import ELFFile
import elftools.dwarf as dwarf

import emit
import serializable

StructMember = namedtuple("StructMember", ["name", "serializer"])

def get_DIEs_depth_first(die):
    yield die
    for child in die.iter_children():
        yield from get_DIEs_depth_first(child)

def get_all_structs(cu):
    structDTagStr = "DW_TAG_structure_type"
    structDTag = dwarf.enums.ENUM_DW_TAG[structDTagStr]

    top = cu.get_top_DIE()
    structs = {
            die.offset : die for die in get_DIEs_depth_first(top)
            if die.tag == structDTagStr
        }

    return structs

def get_serialization_types(structs, CU):
    # TODO: Implement
    types = []
    for struct in structs.values():
        members = []
        for child in struct.iter_children():
            memberName = child.attributes["DW_AT_name"].value.decode(encoding='UTF-8')
            memberSer = serializable.Integer("int", 4, True)
            members.append(StructMember(memberName, memberSer))

        structName = struct.attributes.get("DW_AT_name")
        if structName:
            structName = structName.value.decode(encoding='UTF-8')
        else:
            structName = "object_t"

        types.append(serializable.Aggregate(structName, members))

    return types

def process_file(filename, outfile):
    with open(filename, 'rb') as f:
        elffile = ELFFile(f)

        if not elffile.has_dwarf_info():
            raise IOError("ERROR: {} has no DWARF info".format(filename))

        # get_dwarf_info returns a DWARFInfo context object, which is the
        # starting point for all DWARF-based processing in pyelftools.
        dwarfinfo = elffile.get_dwarf_info()

        with open(outfile, 'w') as outFp:
            for CU in dwarfinfo.iter_CUs():
                structs = get_all_structs(CU)
                types = get_serialization_types(structs, CU)

                emit.emit_serializers(outFp, types)

def get_arg_parser():
    argParser = argparse.ArgumentParser(description='Generates serialization functions for data structures inside an elf file.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argParser.add_argument('elf_file', help="Object file from which to read symbols")
    argParser.add_argument('out_file', type=str, default="/dev/stdout",
            help="Path where the output header will be written")

    return argParser

def main():
    args = get_arg_parser().parse_args()
    process_file(args.elf_file, args.out_file)

if __name__ == "__main__":
    main()
