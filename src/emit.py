def emit_serializers(fp, types):
    fp.write("#include <stdio.h>\n\n")
    fp.write("#define _sERIALIZERS_EMITTED 1\n\n")

    for t in types:
        t.emit_declaration(fp)

    fp.write("\n\n")
    fp.write("/"*80)
    fp.write("\n\n")

    for t in types:
        t.emit_definition(fp)

