import unittest
from unittest.mock import Mock
import os
import pandas as pd
from dateutil.parser._parser import ParserError
from pandas.testing import assert_frame_equal

from parking_recommender import NoParkingSpotsInListError, \
    NoSearchResultsError, InvalidStreetError, ParkingRecommender
from parking_spot import ParkingSpot


class TestParkingRecommender(unittest.TestCase):
    def setUp(self):
        self.filepath = os.path.join(os.path.dirname(__file__),
                            "../data/Annual_Parking_Study_Data_Cleaned2.csv")
        self.test_df = pd.read_csv(self.filepath, low_memory = False)
        self.test_pr = ParkingRecommender(
            [ParkingSpot(0, 0, 'DEXTER AVE N BETWEEN WARD ST AND PROSPECT ST',
                         0, 0)],
            '2021-01-01 12:00:00')

    """Testing the object constructor"""
    def test_raises_No_Parking_Spots_In_List_Error(self):
        test_datetime = '2020-02-04 12:46:29.315237'
        # Parkingspotlist is empty
        self.assertRaises(NoParkingSpotsInListError, ParkingRecommender,
                          [], test_datetime)

    def test_raises_TypeError(self):
        """ParkingSpot is passed invalid datetime format"""
        ps = [ParkingSpot(0, 0, '1ST AVE BETWEEN SENECA ST AND UNIVERSITY ST',
                          0, 0)]
        self.assertRaises((TypeError, ParserError), ParkingRecommender, ps, 
                          'Invalid datetime string')
        self.assertRaises((TypeError, ValueError), ParkingRecommender, ps,
                          '-1')
    
    def test_Annual_Parking_Data_file(self):
        """Make sure normal call doesn't cause exception or errors"""
        pd.read_csv(self.filepath, low_memory = False)
        
    def test_raise_Invalid_Street_Error(self):
        """ParkingSpot list contains a street not in the database"""
        ps_single = [ParkingSpot(0, 0, 'NOT A VALID STREET', 0, 0)]
        ps_multi = [ParkingSpot(0, 0, '1ST AVE BETWEEN SENECA ST AND UNIVERSITY ST',
                                 0, 0),
                    ParkingSpot(0, 0, '1ST AVE BETWEEN PIKE ST AND PINE ST',
                                 0, 0),
                    ParkingSpot(0, 0, 'NOT A VALID STREET', 
                                0, 0)]
        
        self.assertRaises(InvalidStreetError, ParkingRecommender, ps_single,
                          '2020-02-04 12:46:29.315237')
        self.assertRaises(InvalidStreetError, ParkingRecommender, ps_multi,
                          '2020-02-04 12:46:29.315237')

    def test_slice_by_hour(self):
        """slice_by_hour returns properly sliced dataframe"""
        filtered_df = self.test_pr.initial_df[
                self.test_pr.initial_df['Hour'] == self.test_pr.hr]
        
        assert_frame_equal(filtered_df, self.test_pr.slice_by_hour(self.test_pr.hr))
    
    def test_raises_No_Search_Results_Error(self):
        """slice_by_hour raises NoSearchResultsError"""
        self.assertRaises(NoSearchResultsError, self.test_pr.slice_by_hour, 1)

    def test_slice_by_hour_checks_previous_hour(self):
        pass

    def test_slice_by_hour_checks_future_hour(self):
        pass
            

class TestMaxFreeSpace(unittest.TestCase):
    """I can't actually think of any ways this method might fail lol"""
    # @classmethod
    # def setUpClass(cls):
    #     parkingspotlist = [ParkingSpot(0, 0, 'DEXTER AVE N BETWEEN WARD ST AND PROSPECT ST',
    #                       0, 0)]
    #     datetimestring = '2020-02-04 01:46:29.315237'
    #     testing_object = ParkingRecommender(parkingspotlist, datetimestring)
    
    def test_max_freespace(self):
        pass
        # self.assertEquals(testing_object.max_freespace(), (['DEXTER AVE N BETWEEN WARD ST AND PROSPECT ST'], [3]))
        
  
class TestRecommend(unittest.TestCase):

    def test_recommend_raises_exception(self):
        max_freespace = Mock()
        max_freespace.return_value = ([], [])

    def test_output_list(self):
        max_freespace = Mock()
        max_freespace.return_value = ([], []) # put something to test here


if __name__ == "__main__":
    unittest.main()
