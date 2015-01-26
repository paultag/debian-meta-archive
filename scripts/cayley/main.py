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


def cayley(el, data, component, package, version):
    if el is None:
        el = ""
    data = data['Build-Depends']
    relations = data.get("relations", [])
    for relation in relations:
        targets = relation.get("targets", [])
        for target in targets:
            package_bd = target.get("package")
            el += "<{package}> <{relation}> <{target}>\r\n".format(
                package=package,
                relation="build_depends",
                target=package_bd,
            )
    return el


archive.amap(10, "unstable", "main", deps)
data = archive.reduce("main", cayley)

with open("build-depends", "w") as fd:
    fd.write(data)
