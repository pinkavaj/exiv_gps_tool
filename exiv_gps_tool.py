#!/usr/bin/python3

from sys import argv, stdin
from subprocess import Popen, PIPE

class ExivGps:
    class ExivError(ChildProcessError):
        pass


    def __init__(self, file_name):
        self._file_name = file_name

    def get(self):
        """Returns GPS position information or None, if not present"""
        proc = Popen(["exiv2",
                "-g", "Exif.GPSInfo.GPSAltitude",
                "-g", "Exif.GPSInfo.GPSAltitudeRef",
                "-g", "Exif.GPSInfo.GPSLatitude",
                "-g", "Exif.GPSInfo.GPSLatitudeRef",
                "-g", "Exif.GPSInfo.GPSLongitude",
                "-g", "Exif.GPSInfo.GPSLongitudeRef",
                "-g", "Exif.GPSInfo.GPSMapDatum",
                "-g", "Exif.GPSInfo.GPSVersionID",
                self._file_name], stdout=PIPE, universal_newlines=True)
        res = proc.comunicate()[0]
        if proc.returncode is not 0:
            raise ExivError("Nonzero stare returnet from cmd: %s" % repr(proc.returncode))
        res = res.split("\n")
        for r in res:
            r = r.strip()
            if r.startswith("Exif.GPSInfo.GPSLatitude"):
                pass
            elif r.startswith("Exif.GPSInfo.GPSLatitudeRef":
                pass
            elif r.startswith("Exif.GPSInfo.GPSLongitude":
                pass
            elif r.startswith("Exif.GPSInfo.GPSLongitudeRef":
                pass
            else:
                raise ValueError("Invalid exiv2 resutl: %s" % repr(res))
        gps_lat_deg, gps_lat_min, gps_lat_sec = gps_lat.split(' ')
        gps_lat_deg = gps_lat_deg.replace("deg", "")
        gps_lat_min = gps_lat_min.replace("'", "")
        gps_lat_sec = gps_lat_sec.replace('"', "")
        return ((gps_lat_deg, gps_lat_min, gps), (), )

        # TODO: parse result lines

    def set(self, position):
        """Set GPS position information."""
        # todo: check and parse
#49°48'27.876"N, 14°43'4.304"E
        self.lat = lat
        self.long = long
        return call("exiv2",
                "-M set Exif.GPSInfo.GPSLatitude %d/1 %d/1 %d/1" % self.lat[0:3],
                "-M set Exif.GPSInfo.GPSLatitudeRef %s" % self.lat[3:4],
                "-M set Exif.GPSInfo.GPSLongitude %d/1 %d/1 %d/1" % self.long[0:3],
                "-M set Exif.GPSInfo.GPSLongitudeRef %s" % self.long[3:4],
                self._file_name)

def p_help():
    print("Set GPS EXIF information for image files.")
    print("Usage: %s <file> [<file>, <file>, ...]" % argv[0])

if len(argv) < 2:
    p_help()
    exit(1)

def parseGps(gpsTxt):
    """Parse GPS positon information, returns:
    ((lat_deg, lat_min, lat_sec, lat_rel), (long_deg, long_min, long_sec, long_rel))."""


def strGps(gps):
    """Return string representation of GPS coordinates."""
    return """%d°%d'%f"%s %d°%d'%f"%s""" % gps[0] + gps[1]


for file_name in argv[1:]:
    exivGps = ExivGps(file_name)
    gps = exivGps.get()
    if gps:
        gps = strGps(gps)
    else:
        gps = "N/A"
    tabs = 6 - divmod((len(file_name) + 2 + 7), 8)[0]
    if tabs < 0:
        tabs = 0
    tabs = "\t" * tabs
    print("'%s'%s - [%s] :" % (file_name, tabs, gps), end="", flush=True)
    newGps = stdin.readline().strip()
    if newGps:
        newGps = parseGps(newGps)
        exivGps.set(newGps)

