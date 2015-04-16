from dionysus.archive import Archive
import os

archive = Archive("http://192.168.1.50/debian")



def canidate(archive, source, dsc):
    with source.unpack():
        trove_python3 = False
        if os.path.exists("setup.py"):
            buf = open("setup.py", "r").read()
            if "Programming Language :: Python :: 3" in buf:
                trove_python3 = True
    has_python2_module = False
    has_python3_module = False

    for (name, *foo) in filter(lambda x: x != [], (x.strip().split() for x in
            source.source.get('Package-List', "").split("\n"))):
        if name.startswith("python-"): has_python2_module = True
        if name.startswith("python3-"): has_python3_module = True

    return {
        "has_python2_module": has_python2_module,
        "has_python3_module": has_python3_module,
        "trove_python3": trove_python3,
        "canidate": trove_python3 is True and has_python3_module is False
    }

def is_python(source):
    return source.source['Section'] == "python"

archive.amap(10, "unstable", "main", canidate, filter=is_python)
