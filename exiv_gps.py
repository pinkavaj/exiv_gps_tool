
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
            elif tag == "Exif.GPSInfo.GPSVersionID":
                if val < "2.0.0.0":
                    raise ValueError("Unsupported GPSInfo version '%s'" % val)
            elif tag == "Exif.GPSInfo.GPSMapDatum":
                if val != "WGS-84":
                    raise ValueError("Unsupported GPSInfo Datum '%s'" % val)
            else:
                raise ValueError("Invalid exiv2 resutl: %s" % repr(res))

        gps = Gps()
        if gps_lat or gps_lat_ref:
            gps.setLatitude(gps_lat, gps_lat_ref)
        if gps_lon or gps_lon_ref:
            gps.setLongtitude(gps_lon, gps_lon_ref)

        return gps

    def set(self, gps):
        """Set GPS position information."""
        args = ["exiv2", ]
        hasGps = False
        if gps.latitude:
            hasGps = True
            lat = ExivGps._splitDegree(gps.latitude)
            args.append("-M set Exif.GPSInfo.GPSLatitude %d/1 %d/1 %d/100" % lat)
            args.append("-M set Exif.GPSInfo.GPSLatitudeRef %s" % gps.latitude_ref)
        else:
            pass

        if gps.longtitude:
            hasGps = True
            lon = ExivGps._splitDegree(gps.longtitude)
            args.append("-M set Exif.GPSInfo.GPSLongitude %d/1 %d/1 %d/100" % lon)
            args.append("-M set Exif.GPSInfo.GPSLongitudeRef %s" % gps.longtitude_ref)
        else:
            pass

        if gps.altitude:
            hasGps = True
            ref = 0 if gps.altitude >= 0. else 1
            args.append("-M set Exif.GPSInfo.GPSAltitude %d" % abs(round(gps.altitude)))
            args.append("-M set Exif.GPSInfo.GPSAltitudeRef %d" % ref)
        else:
            pass

        if hasGps:
            args.append("-M set Exif.GPSInfo.GPSMapDatum WGS-84")
            args.append("-M set Exif.GPSInfo.GPSVersionID 2 2 0 0")
        else:
            pass

        args.append(self._file_name)
        proc = Popen(args)
        proc.wait()
        if proc.returncode is not 0:
            raise ExivGps.ExivError("Nonzero stare returnet from cmd: %s" % repr(proc.returincode))

    @staticmethod
    def _splitDegree(degrees):
        """Split degrees into tuple, beware, hacked version, see code for details."""
        deg, deg_min = divmod(degrees, 1)
        deg_min, deg_sec = divmod(deg_min*60, 1)
        deg_sec = round(deg_sec*60*100)
        return (deg, deg_min, deg_sec, )
