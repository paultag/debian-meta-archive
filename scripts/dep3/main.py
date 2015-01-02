from dionysus.archive import Archive
from dep3.parse import get_headers
import os

archive = Archive("http://192.168.1.50/debian")


def flatten(path):
    for root, dirs, files in os.walk(path):
        for dpath in dirs:
            yield from flatten(os.path.join(root, dpath))
        yield from (os.path.join(root, x) for x in files)


def report(path):
    with open(path, 'rb') as fd:
        if path.endswith(".patch") or path.endswith(".diff"):
            return get_headers(fd)


def patch(archive, source, dsc):
    print(source.source)
    with source.unpack():
        return {
            "dep3": list(map(report, flatten("debian/patches")))
        }


archive.amap(10, "unstable", "main", patch)
