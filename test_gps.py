#/usr/bin/python3

import unittest
from gps import Gps

class GpsTest(unittest.TestCase):
    pass

    def test__degreesFromString(self):
        coord = Gps._degreesFromString("""38°59'26.348"N""")
        self.assertEqual(len(coord), 2)
        self.assertAlmostEqual(coord[0], 38.99, 2)
        self.assertEqual(coord[1], 'N')

        coord = Gps._degreesFromString("""300.34°N""")
        self.assertEqual(len(coord), 2)
        self.assertAlmostEqual(coord[0], 300.34, 2)
        self.assertEqual(coord[1], 'N')

        self.assertRaises(ValueError, Gps._degreesFromString, """300.34° """)
        self.assertRaises(ValueError,  Gps._degreesFromString, """blah""")

    def test_fromString(self):
        gps = Gps.fromString("""38°59'26.348"N, 5°24'47.948"E""")
        self.assertAlmostEqual(gps.latitude, 38.99, 2);
        self.assertEqual(gps.latitude_ref, 'N')
        self.assertAlmostEqual(gps.longtitude, 5.41, 2)
        self.assertEqual(gps.longtitude_ref, 'E')
        self.assertEqual(gps.altitude, None)

        self.assertRaises(ValueError, Gps.fromString, "blah")


if __name__ == '__main__':
        unittest.main()
