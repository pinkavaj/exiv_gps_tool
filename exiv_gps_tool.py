#!/usr/bin/python3

from gps import Gps
from exiv_gps import ExivGps
from sys import argv, stdin


class ExivGpsTool:
    def __init__(self):
        pass

    def process(self, file_name):
        exivGps = ExivGps(file_name)
        try:
            gps = exivGps.get()
            if gps:
                gps = gps.toString()
            else:
                gps = "N/A"
        except ExivGps.ExivError:
            print("Failed to get exif information, skipping: '%s'" % file_name)
            return

        tabs = 6 - divmod((len(file_name) + 2 + 7), 8)[0]
        if tabs < 0:
            tabs = 0
        tabs = "\t" * tabs
        print("'%s'%s - [%s] : " % (file_name, tabs, gps), end="", flush=True)
        newGps = stdin.readline().strip()
        if newGps:
            newGps = Gps.fromString(newGps, gps)
            exivGps.set(newGps)

    @staticmethod
    def p_help():
        print("Set GPS EXIF information for image files.")
        print("Usage: %s <file> [<file>[ <file> [...]]]" % argv[0])


if __name__ == '__main__':
    if len(argv) < 2:
        ExivGpsTool.p_help()
        exit(1)

    tool = ExivGpsTool()
    for file_name in argv[1:]:
        tool.process(file_name)
