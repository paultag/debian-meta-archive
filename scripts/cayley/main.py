from debversion import Block
from dionysus.archive import Archive
import os

archive = Archive("http://192.168.1.50/debian")


def deps(archive, source, dsc):
    deps = dsc['Build-Depends']
    data = {
        "Build-Depends": Block(dsc['Build-Depends']).to_dict()
    }
    return data


archive.amap(10, "unstable", "main", deps)
