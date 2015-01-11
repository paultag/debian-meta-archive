from dionysus.util import run_command
from dionysus.archive import Archive
import os

archive = Archive("http://192.168.1.50/debian")


def patch(archive, source, dsc):
    print(" -> %s" % (dsc['Source']))

    os.mkdir("uscan")
    with source.unpack():
        version = dsc['Version']
        if '-' not in version:
            return

        upstream, debian = version.rsplit("-", 1)

        print("Uscan'ing")
        out, err, ret = run_command([
            "uscan",
                "--force-download",
                "--download-version", upstream,
                "--destdir", "../uscan/"
        ])
        print("Uscan'd")
        if ret != 0:
            print("Error: %s/%s - %s" % (
                dsc['Source'],
                dsc['Version'],
                ret,
            ))
            return

    out, err, ret = run_command(['ls', '-l', 'uscan'])
    print(out.decode('utf-8'))


archive.map("unstable", "main", patch, test=True)
