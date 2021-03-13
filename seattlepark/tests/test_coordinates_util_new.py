import unittest
from unittest.mock import Mock, patch
from coordinates_util import CoordinatesUtil


class Coordinate:

    def __init__(self, lat, long):
        self.latitude = lat
        self.longitude = long


class CoordinatesUtilTest(unittest.TestCase):

    def test_sea_parking_geocode(self):
        cu = CoordinatesUtil()
        coordinates_mapping = cu.sea_parking_geocode()
        self.assertTrue(len(coordinates_mapping) > 0)
        for key, value in coordinates_mapping.items():
            self.assertTrue(key is not None)
            self.assertTrue(value is not None)
            self.assertEqual(len(value), 2)
            self.assertEqual(len(value[0]), 2)
            self.assertEqual(len(value[1]), 2)

    def test_get_destination_coordinates(self):
        cu = CoordinatesUtil()
        # Mock member variable geo_locator of CoordinatesUtil
        cu.geo_locator = Mock()
        # Mock geocode on the mocked member variable geo_locator to return value as Coordinate(Point(1.1, 1.2)).
        cu.geo_locator.geocode.return_value = Coordinate(1.1, 1.2)

        coordinates = cu.get_destination_coordinates("Some Address")
        self.assertEqual(coordinates, [1.1, 1.2])


if __name__ == "__main__":
    unittest.main()
