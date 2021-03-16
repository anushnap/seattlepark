import unittest
import os
import pandas as pd
from dateutil.parser._parser import ParserError
from pandas.testing import assert_frame_equal

from parking_recommender import NoParkingSpotsInListError, \
    NoSearchResultsError, InvalidStreetError, ParkingRecommender
from parking_spot import ParkingSpot


class TestParkingRecommender(unittest.TestCase):
    def setUp(self):
        """
        Create test_df and ParkingRecommender with 1 address and
        2021/01/01 12:00:00 PM as time.
        """
        self.filepath = os.path.join(
            os.path.dirname(__file__),
            "../src/resources/Annual_Parking_Study_Data_Cleaned2.csv")
        self.test_df = pd.read_csv(self.filepath, low_memory=False)
        self.test_street = 'DEXTER AVE N BETWEEN WARD ST AND PROSPECT ST'
        self.test_ps = ParkingSpot(0, 0, self.test_street, 0, 0)
        self.test_pr = ParkingRecommender(
            [self.test_ps],
            '2021-01-01 12:00:00'
        )

    """Testing the object constructor"""

    def test_raises_No_Parking_Spots_In_List_Error(self):
        test_datetime = '2020-02-04 12:46:29.315237'
        # Parkingspotlist is empty
        self.assertRaises(NoParkingSpotsInListError, ParkingRecommender,
                          [], test_datetime)

    def test_raises_TypeError(self):
        """ParkingSpot is passed invalid datetime format"""
        self.assertRaises((TypeError, ParserError),
                          ParkingRecommender,
                          self.test_ps,
                          'Invalid datetime string')
        self.assertRaises((TypeError, ValueError),
                          ParkingRecommender,
                          self.test_ps,
                          '-1')

    def test_Annual_Parking_Data_file(self):
        """Make sure normal call doesn't cause exception or errors"""
        pd.read_csv(self.filepath, low_memory=False)

    def test_raise_Invalid_Street_Error(self):
        """ParkingSpot list contains a street not in the database"""
        ps_single = [ParkingSpot(0, 0, 'NOT A VALID STREET', 0, 0)]
        ps_multi = [ParkingSpot(0, 0,
                                '1ST AVE BETWEEN SENECA ST AND UNIVERSITY ST',
                                0, 0),
                    ParkingSpot(0, 0,
                                '1ST AVE BETWEEN PIKE ST AND PINE ST',
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

        assert_frame_equal(filtered_df,
                           self.test_pr.slice_by_hour(self.test_pr.hr))

    def test_raises_No_Search_Results_Error(self):
        """slice_by_hour raises NoSearchResultsError"""
        self.assertRaises(
            NoSearchResultsError, self.test_pr.slice_by_hour, 1)
        self.assertRaises(
            NoSearchResultsError, self.test_pr.slice_by_hour, 5)
        self.assertRaises(
            NoSearchResultsError, self.test_pr.slice_by_hour, 22)

    def test_slice_by_hour_returns_previous_hour(self):
        """slice_by_hour returns drataframe sliced to previous hour
        when passed hour lacks data"""
        prev_hour_df = self.test_pr.initial_df[
            self.test_pr.initial_df['Hour'] == 20]
        assert_frame_equal(prev_hour_df, self.test_pr.slice_by_hour(21))

    def test_slice_by_hour_returns_future_hour(self):
        """slice_by_hour returns dataframe sliced to next available hour
        when passed hour lacks data"""
        next_hour_df = self.test_pr.initial_df[
            self.test_pr.initial_df['Hour'] == 8]
        assert_frame_equal(next_hour_df, self.test_pr.slice_by_hour(7))

    def test_max_freespace(self):
        self.assertEqual(
            self.test_pr.max_freespace(),
            (['DEXTER AVE N BETWEEN WARD ST AND PROSPECT ST'], [3])
        )


class TestRecommend(unittest.TestCase):
    def setUp(self):
        self.filepath = \
            os.path.join(os.path.dirname(__file__),
                         "../src/resources/Annual_Parking_Study_Data_Cleaned2.csv")
        self.test_df = pd.read_csv(self.filepath, low_memory=False)
        self.test_ps1 = ParkingSpot(
            1, [[1, 3], [2, 4]],
            "1ST AVE BETWEEN SENECA ST AND UNIVERSITY ST", 1, 1
        )
        self.test_ps2 = ParkingSpot(
            1, [[1, 3], [2, 4]],
            'DEXTER AVE N BETWEEN WARD ST AND PROSPECT ST', 1, 1
        )
        self.test_pr = ParkingRecommender(
            [self.test_ps1, self.test_ps2], '2021-01-01 12:00:00'
        )

    def test_recommend(self):
        return_list = self.test_pr.recommend()
        self.assertEqual(
            return_list[0].street_name,
            self.test_ps1.street_name
        )
        self.assertEqual(
            return_list[1].street_name,
            self.test_ps2.street_name
        )

    def test_recommend_raises_exception(self):
        """check that recommend() returns the 5 closest if no data within
        +/- 1 hour of desired time"""
        # the 5 closest in this list are inp_list[1:]
        inp_list = [
            ParkingSpot(10, [[1, 3], [2, 4]],
                        '12TH AVE BETWEEN E SPRING ST AND E MADISON ST',
                        1, 1),
            ParkingSpot(1, [[1, 3], [2, 4]],
                        '12TH AVE BETWEEN E CHERRY ST AND E COLUMBIA ST',
                        1, 1),
            ParkingSpot(1, [[1, 3], [2, 4]],
                        '12TH AVE BETWEEN E COLUMBIA ST AND E MARION ST',
                        1, 1),
            ParkingSpot(1, [[1, 3], [2, 4]],
                        '12TH AVE BETWEEN E JAMES CT AND E CHERRY ST',
                        1, 1),
            ParkingSpot(1, [[1, 3], [2, 4]],
                        '12TH AVE BETWEEN E JEFFERSON ST AND E BARCLAY CT',
                        1, 1),
            ParkingSpot(1, [[1, 3], [2, 4]],
                        '12TH AVE BETWEEN E MARION ST AND E SPRING ST',
                        1, 1)
        ]
        # We know there are no observations between 00:00 and 08:00
        # so it should just return the 5 closest
        test_pr2 = ParkingRecommender(inp_list, '2021-01-01 04:00:00')
        return_list = test_pr2.recommend()
        self.assertEqual(return_list, inp_list[1:])


if __name__ == "__main__":
    unittest.main()
