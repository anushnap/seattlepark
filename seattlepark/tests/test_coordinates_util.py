import unittest
from unittest.mock import Mock
from coordinates_util import CoordinatesUtil
import pandas as pd
import numpy as np
import haversine as hs
import base64
import os
import sys

class TestCoordinate:

    def __init__(self, lat, long):
        self.latitude = lat
        self.longitude = long


class CoordinatesUtilTest(unittest.TestCase):

    def setUp(self):
        self.cu = CoordinatesUtil()
    
    def test_cal_distance(self):
        """Calcs haversine distance on tuple"""
        test_loc1 = (45.8, 4.8)
        test_loc2 = (48.9, 2.4)

        self.assertEqual(hs.haversine(test_loc1, test_loc2, unit = "mi"),
                         self.cu.cal_distance(test_loc1, test_loc2))
    
    def test_cal_distance_takes_list(self):
        """Calcs haversine distance on list"""
        test_loc1 = [45.8, 4.8]
        test_loc2 = [48.9, 2.4]

        self.assertEqual(hs.haversine(test_loc1, test_loc2, unit = "mi"),
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
    
    # def test_cal_distance_raises_value_error(self):
    #     """Raise ValueError when passed iterables > 2"""

    #     self.assertRaises(ValueError, 
    #                       self.cu.cal_distance, (1, 2, 3), (1, 2, 3))
    #     self.assertRaises(ValueError, 
    #                       self.cu.cal_distance, [1, 2, 3], [1, 2, 3])
    
    # def test_cal_distance_raises_type_error(self):
    #     """Raise TypeError when passed strings"""
    #     self.assertRaises(TypeError, 
    #                       self.cu.cal_distance, ('1', '2'), (1, 2))
    #     self.assertRaises(TypeError,
    #                       self.cu.cal_distance, (1, 2), ('1', '2'))

    def test_get_parking_spots_returns_none(self):
        """get_parking_spots returns empty list when nothing meets critera"""
        spots, white_house = self.cu.get_parking_spots(
                "1600 Pennsylvania Avenue, N.W. Washington, DC 20500", 1)
        self.assertEqual([], spots)
        self.assertEqual(None, white_house)

    def test_get_parking_spots_handles_exception(self):
        pass

    def test_sea_parking_geocode(self):
        coordinates_mapping = self.cu.sea_parking_geocode()
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

