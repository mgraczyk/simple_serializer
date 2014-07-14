from itertools import repeat

class Serializable(object):
    def __init__(self, name):
        self.name = name
        pass

    def emit_declaration(self, fp):
        fp.write(self._get_prototype() + ";\n")

    def emit_definition(self, fp):
        raise NotImplementedError()

    def get_serialization_code(self):
        raise NotImplementedError()

    def _get_serializer_name(self):
        return "simple_serialize_{0}".format(self.name)

    def _get_prototype(self):
        fmt = "void {0}(const {1} * obj, FILE * fp)"
        proto = fmt.format(self._get_serializer_name(), self.name)
        return proto

class Aggregate(Serializable):
    def __init__(self, name, members):
        super().__init__(name)
        self.members = members

    def emit_definition(self, fp):
        fp.write(self._get_prototype() + "\n{\n")

        fp.write('fputs("{", fp);\n')
        fp.write('fputs(",", fp);\n'.join(map(self._get_member_serializer, self.members)))
        fp.write('fputs("}", fp);\n')

        fp.write("}\n\n")

    def get_serialization_code(self, obj):
        return "{}(&{}, fp);".format(self._get_serializer_name(), obj)

    def _get_member_serializer(self, member):
        memberSerializer = member.serializer.get_serialization_code("obj->" + member.name)
        return 'fputs("\\"{}\\":", fp);\n{}\n'.format(member.name, memberSerializer)

class FPrintfable(Serializable):
    def __init__(self, name, fmtSpc):
        super().__init__(name)
        self.fmtSpc = fmtSpc 

    def get_serialization_code(self, obj):
        return r'fprintf(fp, "{}", {});'.format(self.fmtSpc, obj)

class Integer(FPrintfable):
    SizeSpcs = {
            1: "hh",
            2: "h",
            4: "",
            8: "ll"
            }

    def __init__(self, name, size, signed):
        super().__init__(name, self._get_fmt_spc(size, signed))
        self.size = size
        self.signed = signed

    def emit_declaration(self, fp):
        pass

    def emit_definition(self, fp):
        pass

    def _get_fmt_spc(self, size, signed):
        sizeSpc = self.SizeSpcs.get(size)
        if sizeSpc == None:
            raise NotImplementedError("Size {} integer not implemented.".format(size))

        signedSpc = "d" if signed else "u"
        return "%" + sizeSpc + signedSpc

class QuotedPrimitive(FPrintfable):
    def __init__(self, name, fmtSpc):
        super().__init__(name, '\\"' + fmtSpc + '\\"')

class Char(QuotedPrimitive):
    def __init__(self):
        super().__init__("char", "%c")

class String(QuotedPrimitive):
    def __init__(self):
        super().__init__("const char *", "%s")

class Array(Serializable):
    def __init__(self, name, numelem):
        super().__init__(name)
        self.numelem = numelem

    def emit_declaration(self, fp):
        pass

    def emit_definition(self, fp):
        pass

    def get_serialization_code(self, obj):
        raise NotImplementedError()
