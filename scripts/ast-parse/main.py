from dionysus.archive import Archive
import ast
import os

archive = Archive("http://archive.paultag.house/debian")


class LoggerVisitor(ast.NodeVisitor):
    found = []

    def _attr_to_str(self, obj):
        if isinstance(obj, ast.Attribute):
            return "{}.{}".format(self._attr_to_str(obj.value), obj.attr)
        if isinstance(obj, ast.Name):
            return obj.id
        if isinstance(obj, ast.Str):
            return '"{}"'.format(obj.s)
        return "<unknown>"

    def visit(self, node):
        super(LoggerVisitor, self).visit(node)
        return self.found

    def visit_Call(self, node):
        function = self._attr_to_str(node.func)
        if function.startswith("logging."):
            self.found.append(", ".join([function, *map(self._attr_to_str, node.args)]))


def parse(reader):
    try:
        x = LoggerVisitor().visit(ast.parse(reader.read()))
        # print(x)
        return x
    except SyntaxError:
        # Python 2...
        return


def canidate(archive, source, dsc):
    if not is_python(source):
        return

    ret = {}
    with source.unpack():
        for dirpath, dirnames, filenames in os.walk("."):
            for filename in filenames:
                if not filename.endswith(".py"):
                    continue
                path = os.path.join(dirpath, filename)
                with open(path) as fd:
                    ret[path] = parse(fd)
    return ret

def is_python(source):
    return source.source['Section'] == "python"

archive.amap(40, "unstable", "main", canidate)
