import unittest
from unittest.mock import Mock
from seattlepark.src.coordinates_util import CoordinatesUtil
import pandas as pd
import numpy as np
import haversine as hs

class CoordinatesUtilTest(unittest.TestCase):

    def test_cal_distance(self):
        test_loc1 = (45.8, 4.8)
        test_loc2 = (48.9, 2.4)

        # Can I actually use mock like this in calls that require "self"?
        # I've done it this way to avoid having to open and access the API key
        # and without having to go in and change Qiaohio's code and
        # accidentally cause merge conflicts down the road
        self.assertEqual(hs.haversine(test_loc1, test_loc2, unit = "mi"),
                         CoordinatesUtil.cal_distance(Mock(), test_loc1, test_loc2))
    
    # GET QIAOHUIS HELP
    def test_get_destination_coordinates(self):
        pass

    def test_get_parking_spots(self):
        pass


if __name__ == "__main__":
    unittest.main()

