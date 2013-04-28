
class Gps:
    """GPS coordinate representation."""
    def __init__(self):
        self.altitude = self.latitude_ref = None
        self.latitude = self.longtitude_ref = None
        self.longtitude = None

    def __str__(self):
        if self.longtitude is None and self.longtitude_ref is None and \
                self.latitude is None and self.latitude_ref is None and \
                self.altitude is None:
            return "N/A"
        s = ""
        if self.latitude is None and self.latitude_ref is None:
            s += "N/A, "
        else:
            s += Gps._degreesToString(self.latitude) + self.latitude_ref + ", "

        if self.longtitude is None and self.longtitude_ref is None:
            s += "N/A, "
        else:
            s += Gps._degreesToString(self.longtitude) + self.longtitude_ref + ", "

        if self.altitude is None:
            s += "N/A"
        else:
            s += str(self.altitude)
        return s

    def setLatitude(self, degrees, ref):
        if degrees is None and ref is None:
            self.latitude = self.latitude_ref = None
            return
        if ref not in ("N", "S", ):
            raise ValueError("Invalid reference value '%s'." % repr(ref))
        if not (degrees >= 0. and degrees <= 180.):
            raise ValueError("Invalid latitude degree value.")
        self.latitude = degrees
        self.latitude_ref = ref

    def setLongtitude(self, degrees, ref):
        if degrees is None and ref is None:
            self.longtitude = self.longtitude_ref = None
            return
        if ref not in ("E", "W", ):
            raise ValueError("Invalid reference value '%s'." % repr(ref))
        if not (degrees >= 0. and degrees <= 180.):
            raise ValueError("Invalid longtitude degree value.")
        self.longtitude = degrees
        self.longtitude_ref = ref

    def setAltitude(self, altitude):
        self.altitude = altitude

    @staticmethod
    def fromString(position, gps_defaults=None):
        """Create Gps position object from text representation."""
        position = [p.strip() for p in position.split(",")]
        if len(position) > 3 or not len(position):
            raise ValueError("Invalid position string format: '%s'." % repr(position))
        if len(position) == 1:
            if position[0] != "N/A":
                raise ValueError("Invalid position string format: '%s'." % repr(position))
            return Gps()

        gps = gps_defaults if gps_defaults is not None else Gps()

        if position[0] == "N/A":
            gps.setLatitude(None, None)
        else:
            lat, lat_ref = Gps._posAndRefFromString(position[0])
            gps.setLatitude(lat, lat_ref)

        if position[1] == "N/A":
            gps.setLongtitude(None, None)
        else:
            lon, lon_ref = Gps._posAndRefFromString(position[1])
            gps.setLongtitude(lon, lon_ref)

        if len(position) == 3:
            if position[2] == "N/A":
                gps.setAltitude(None)
            else:
                gps.setAltitude(float(position[2]))

        return gps

    @staticmethod
    def _posAndRefFromString(position):
        position = position.strip()
        ref = position[-1]
        return (Gps._degreesFromString(position[:-1].strip()), ref, )

    @staticmethod
    def _degreesFromString(degrees):
        """Converts degrees from string into float, eg 38°59'26.348" -> 38.99"""
        deg, deg_min = degrees.split('°')
        deg = float(deg)
        if deg_min:
            deg_min, deg_sec = deg_min.split("'")
            deg += float(deg_min) / 60.
            if deg_sec:
                deg_sec, garabage = deg_sec.split('"')
                if garabage.strip():
                    raise ValueError("Invalid degree format")
                deg += float(deg_sec) / 3600.
        return deg

    @staticmethod
    def _degreesToString(degrees):
        deg, deg_min = divmod(degrees, 1)
        deg_min, deg_sec = divmod(deg_min * 60, 1)
        deg_sec *= 60
        return "%d°%d'%f\"" % (deg, deg_min, deg_sec)
