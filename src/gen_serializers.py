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

def get_dies_by_offset(cu):
    top = cu.get_top_DIE()
    return { die.offset : die for die in get_DIEs_depth_first(top) }

def get_struct_dies(diesByOffset):
    structDTagStr = "DW_TAG_structure_type"
    structDTag = dwarf.enums.ENUM_DW_TAG[structDTagStr]

    structs = dict(p for p in diesByOffset.items()
            if p[1].tag == structDTagStr )#and p[1].attributes.get("DW_AT_name"))

    return structs

def get_base_type(diesByOffset, die):
    typeAttr = die.attributes.get("DW_AT_type")
    while typeAttr != None:
        die = diesByOffset[typeAttr.value]
        typeAttr = die.attributes.get("DW_AT_type")
    return die

def get_serialization_types(types, CU):
    diesByOffset = get_dies_by_offset(CU)
    structs = get_struct_dies(diesByOffset)

    # TODO: Implement
    serializers = []
    for t in types:
        members = []
        for child in struct.iter_children():
            memberName = child.attributes["DW_AT_name"].value.decode(encoding='UTF-8')
            memberType = get_base_type(diesByOffset, child)

            if memberType.tag != "DW_TAG_base_type":
                continue

            memberTypeName = memberType.attributes["DW_AT_name"].value.decode(encoding='UTF-8')
            memberTypeSize = memberType.attributes["DW_AT_byte_size"].value
            memberSer = serializable.Integer(memberTypeName, memberTypeSize, True)
            members.append(StructMember(memberName, memberSer))

        structName = struct.attributes.get("DW_AT_name")
        if structName:
            structName = structName.value.decode(encoding='UTF-8')
        else:
            structName = "object_t"

        serializers.append(serializable.Aggregate(structName, members))

    return serializers

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
                dies = get_dies_by_offset(CU)
                types = get_serialization_types(CU)

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
