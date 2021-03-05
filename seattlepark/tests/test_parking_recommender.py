import unittest
import os
import pandas as pd
from dateutil.parser._parser import ParserError
# import sys
# from pandas.util.testing import assert_frame_equal # <-- for testing dataframes

"""Anushna, can you help me with this part please, i need to import the ParkingRecommender and ParkingSpot modules"""
from seattlepark.parking_recommender import NoParkingSpotsInListError, NoSearchResultsError, InvalidStreetError, ParkingRecommender
from seattlepark.src.parking_spot import ParkingSpot


class TestRecommenderInit(unittest.TestCase):
    """Testing the object constructor"""
    def test_raises_No_Parking_Spots_In_List_Error(self):
        """ParkingSpot list is empty"""
        with self.assertRaises(NoParkingSpotsInListError):
            pr_obj = ParkingRecommender([], '2020-02-04 12:46:29.315237')

    def test_raises_TypeError(self):
        """ParkingSpot is passed invalid datetime format"""
        ps = [
            ParkingSpot(0, 0, '1ST AVE BETWEEN SENECA ST AND UNIVERSITY ST', 0, 0)
            ]
        with self.assertRaises((TypeError, ParserError)):
            pr_obj = ParkingRecommender(ps, 'Invalid datetime string')
        
        with self.assertRaises((TypeError, ValueError)):
            pr_obj = ParkingRecommender(ps, '-1')

        with self.assertRaises((TypeError, NoSearchResultsError)):
            pr_obj = ParkingRecommender(ps, -1)


class TestDataSlice(unittest.TestCase):
    """Testing ParkingRecommender.slice_df()"""
    def test_raise_Invalid_Street_Error(self):
        """ParkingSpot list contains a street not in the database"""
        with self.assertRaises(InvalidStreetError):
            ps = [
                ParkingSpot(0, 0, '1ST AVE BETWEEN SENECA ST AND UNIVERSITY ST', 0, 0),
                ParkingSpot(0, 0, '1ST AVE BETWEEN PIKE ST AND PINE ST', 0, 0),
                ParkingSpot(0, 0, 'NOT A VALID STREET', 0, 0)
                ]
            pr_obj = ParkingRecommender(ps, '2020-02-04 12:46:29.315237')

    def test_raises_No_Search_Results_Error(self):
        """No observations available for the streets/hour combination selected"""
        with self.assertRaises(NoSearchResultsError):
            ps = [
                ParkingSpot(0, 0, '1ST AVE BETWEEN SENECA ST AND UNIVERSITY ST', 0, 0),
                ParkingSpot(0, 0, '1ST AVE BETWEEN PIKE ST AND PINE ST', 0, 0),
                ParkingSpot(0, 0, '1ST AVE W BETWEEN W JOHN ST AND W THOMAS ST', 0, 0)
                ]
            # Presumably there are no observations at 1 AM...
            pr_obj = ParkingRecommender(ps, '2020-02-04 01:46:29.315237')


class TestMaxFreeSpace(unittest.TestCase):
    """I can't actually think of any ways this method might fail lol"""
    pass


if __name__ == "__main__":
    unittest.main()
