
from gps import Gps
from subprocess import Popen, PIPE

class ExivGps:
    """Read/write GPS information from image EXIF data."""

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
        res = proc.communicate()[0]
        if proc.returncode is not 0 and proc.returncode is not 253:
            raise ExivGps.ExivError("Nonzero stare returnet from cmd: %s" % repr(proc.returncode))

        lines = res.splitlines()
        gps_lat = gps_lat_ref = None
        gps_lon = gps_lon_ref = None
        for line in lines:
            line = [l for l in line.split(' ') if l]
            line = line[0:3] + [' '.join(line[3:]), ]
            tag, form, num, val = line
            if tag == "Exif.GPSInfo.GPSLatitude":
                gps_lat = Gps._degreesFromString(val.replace('deg', '°'))
            elif tag == "Exif.GPSInfo.GPSLatitudeRef":
                gps_lat_ref = {'North': 'N', 'South': 'S', }[val]
            elif tag == "Exif.GPSInfo.GPSLongitude":
                gps_lon = Gps._degreesFromString(val.replace('deg', '°'))
            elif tag == "Exif.GPSInfo.GPSLongitudeRef":
                gps_lon_ref = {'East': 'E', 'West': 'W', }[val]
            elif tag == "Exif.GPSInfo.GPSAltitude":
                gps_alt = val
            else:
                raise ValueError("Invalid exiv2 resutl: %s" % repr(res))

        gps = Gps()
        if gps_lat or gps_lat_ref:
            gps.setLatitude(gps_lat, gps_lat_ref)
        if gps_lon or gps_lon_ref:
            gps.setLongtitude(gps_lon, gps_lon_ref)

        return gps

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

