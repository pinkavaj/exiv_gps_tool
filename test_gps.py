#/usr/bin/python3

import unittest
from gps import Gps

class GpsTest(unittest.TestCase):
    pass

    def test__degreesFromString(self):
        degrees = Gps._degreesFromString("""38°59'26.348\"""")
        self.assertAlmostEqual(degrees, 38.99, 2)

        degrees = Gps._degreesFromString("""300.34°""")
        self.assertAlmostEqual(degrees, 300.34, 2)

        self.assertRaises(ValueError, Gps._degreesFromString, """300.34° """)
        self.assertRaises(ValueError,  Gps._degreesFromString, """blah""")

    def test_fromString(self):
        gps = Gps.fromString("""38°59'26.348"N, 5°24'47.948"E""")
        self.assertAlmostEqual(gps.latitude, 38.99, 2);
        self.assertEqual(gps.latitude_ref, 'N')
        self.assertAlmostEqual(gps.longtitude, 5.41, 2)
        self.assertEqual(gps.longtitude_ref, 'E')
        self.assertEqual(gps.altitude, None)

        gps = Gps.fromString("""38°59'26.348"N, 5°24'47.948"E, 254""")
        self.assertAlmostEqual(gps.latitude, 38.99, 2);
        self.assertEqual(gps.latitude_ref, 'N')
        self.assertAlmostEqual(gps.longtitude, 5.41, 2)
        self.assertEqual(gps.longtitude_ref, 'E')
        self.assertEqual(gps.altitude, 254.)

        self.assertRaises(ValueError, Gps.fromString, "blah")


if __name__ == '__main__':
        unittest.main()
