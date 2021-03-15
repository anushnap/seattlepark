import unittest
from unittest.mock import Mock
from coordinates_util import CoordinatesUtil
import haversine as hs
import base64
import os
import sys
import pandas as pd


class TestCoordinate:

    def __init__(self, lat, long):
        self.latitude = lat
        self.longitude = long


class CoordinatesUtilTest(unittest.TestCase):

    def setUp(self):
        self.cu = CoordinatesUtil()

    def test_json_file_loads(self):
        """Normal call of json file does not raise issues or exceptions"""
        filepath = os.path.join(
                os.path.dirname(__file__),
                '../src/resources/Midpoints_and_LineCoords.json')
        with open(filepath) as json:
            pass

    def test_key_file_loads(self):
        """Normal call of encoded key file does not raise exceptions"""
        filepath = os.path.join(
            os.path.dirname(__file__),
            '../src/resources/google_map_api.key')

        with open(filepath) as key:
            pass

    def test_cal_distance(self):
        """Calcs haversine distance on tuple"""
        test_loc1 = (45.8, 4.8)
        test_loc2 = (48.9, 2.4)

        self.assertEqual(hs.haversine(test_loc1, test_loc2, unit="mi"),
                         self.cu.cal_distance(test_loc1, test_loc2))

    def test_cal_distance_takes_list(self):
        """Calcs haversine distance on list"""
        test_loc1 = [45.8, 4.8]
        test_loc2 = [48.9, 2.4]

        self.assertEqual(hs.haversine(test_loc1, test_loc2, unit="mi"),
                         self.cu.cal_distance(test_loc1, test_loc2))

    def test_cal_distance_catches_exception(self):
        """Returns sys.maxsize when exception is raised"""
        self.assertEqual(self.cu.cal_distance((1, 2, 3), (1, 2, 3)),
                         sys.maxsize)
        self.assertEqual(self.cu.cal_distance([1, 2, 3], [1, 2, 3]),
                         sys.maxsize)
        self.assertEqual(self.cu.cal_distance(('1', '2'), (1, 2)),
                         sys.maxsize)
        self.assertEqual(self.cu.cal_distance((1, 2), ('1', '2')),
                         sys.maxsize)
        self.assertEqual(self.cu.cal_distance("(1, 2)", (1, 2)),
                         sys.maxsize)

    def test_get_parking_spots_returns_none(self):
        """get_parking_spots returns empty list when nothing meets critera"""
        spots, white_house = self.cu.get_parking_spots(
            "1600 Pennsylvania Avenue, N.W. Washington, DC 20500", 1)
        self.assertEqual([], spots)
        self.assertEqual(None, white_house)

    def test_get_parking_spots_handles_exception(self):
        pass

    def test_sea_parking_geocode(self):
        """Test validity of key, value pairs of coordinates_mapping"""
        filepath = os.path.join(
                os.path.dirname(__file__),
                '../data/Annual_Parking_Study_Data_Cleaned2.csv')
        parking_data = pd.read_csv(filepath, low_memory=False)
        streets = parking_data['Unitdesc'].unique()
        coordinates_mapping = self.cu.sea_parking_geocode()
        self.assertTrue(len(coordinates_mapping) > 0)
        for key, value in coordinates_mapping.items():
            self.assertTrue(key is not None)
            self.assertTrue(value is not None)
            self.assertEqual(len(value), 2)
            self.assertEqual(len(value[0]), 2)
            self.assertEqual(len(value[1]), 2)
            self.assertTrue(key in streets)

    def test_sea_parking_geocode_returns_coordinates_mapping(self):
        test_dict = {'List': [1, 2, 3], 'List 2': [2, 3, 4]}
        self.cu.coordinates_mapping = test_dict
        self.assertDictEqual(test_dict, self.cu.sea_parking_geocode())

    def test_get_destination_coordinates(self):
        cu = CoordinatesUtil()
        # Mock member variable geo_locator of CoordinatesUtil
        cu.geo_locator = Mock()
        # Mock geocode on the mocked member variable geo_locator to return
        # as Coordinate(Point(1.1, 1.2)).
        cu.geo_locator.geocode.return_value = TestCoordinate(1.1, 1.2)

        coordinates = cu.get_destination_coordinates("Some Address")
        self.assertEqual(coordinates, [1.1, 1.2])

    # SHOULD I TEST THIS? THIS BASICALLY ENDS UP DOING THE EXACT SAME CODE....
    def test_decode_data(self):
        path = os.path.join(os.path.dirname(__file__), "data/test_key.key")
        key = self.cu.decode_data("../tests/data/test_key.key")

        with open(path) as handle:
            encoded_bytes = handle.read().encode('ascii')
            decoded_bytes = base64.b64decode(encoded_bytes)

        self.assertEqual(decoded_bytes.decode("ascii"), key)


if __name__ == "__main__":
    unittest.main()
