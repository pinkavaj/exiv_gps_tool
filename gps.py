
class Gps:
    """GPS coordinate representation."""
    def __init__(self):
        self.altitude = None
        self.latitude = None
        self.longtitude = None

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
            raise ValueError("Invalid reference value.")
        if not (degrees >= 0. and degrees <= 180.):
            raise ValueError("Invalid longtitude degree value.")
        self.longtitude = degrees
        self.longtitude_ref = ref

    def setAltitude(self, altitude):
        self.altitude = altitude

    @classmethod
    def fromString(cls, position):
        """Create Gps position object from text representation."""
        position = position.split(",")
        if len(position) > 3:
            raise ValueError("Invalid position format. too much ','.")
        lat, lat_ref = Gps._posAndRefFromString(position[0])
        lon, lon_ref = Gps._posAndRefFromString(position[1])

        gps = Gps()
        gps.setLatitude(lat, lat_ref)
        gps.setLongtitude(lon, lon_ref)
        if len(position) == 3:
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

