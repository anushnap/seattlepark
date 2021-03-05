import unittest
import os
import pandas as pd
from pandas.util.testing import assert_frame_equal # <-- for testing dataframes
import seattlepark.slice_df as slc

class TestDataSlice(unittest.TestCase):

    def test_raises_Invalid_Area_Exception(self):
        self.assertRaises(slc.InvalidAreaError, slc.slice_df, 'Invalid neighborhood', 'any', 0)


    def test_raises_Invalid_DayType_Exception(self):
        self.assertRaises(slc.InvalidDayTypeError, slc.slice_df, 'Ballard', 'Monday', 0)
        self.assertRaises(slc.InvalidDayTypeError, slc.slice_df, 'Ballard', 1, 0)


    def test_raises_Invalid_Time_Exception(self):
        self.assertRaises(slc.InvalidTimeError, slc.slice_df, 'Ballard', 'any', 24)
        self.assertRaises(slc.InvalidTimeError, slc.slice_df, 'Ballard', 'any', -1)
        self.assertRaises(slc.InvalidTimeError, slc.slice_df, 'Ballard', 'any', '0')
        self.assertRaises(slc.InvalidTimeError, slc.slice_df, 'Ballard', 'any', 0.0)


    def test_raises_No_Search_Results_Exception(self):
        self.assertRaises(slc.NoSearchResultsError, slc.slice_df, '12th Ave', 'any', 3)
        self.assertRaises(slc.NoSearchResultsError, slc.slice_df, 'Denny Triangle', 'weekday', 4)
        self.assertRaises(slc.NoSearchResultsError, slc.slice_df, 'First Hill', 'weekend', 5)
        self.assertRaises(slc.NoSearchResultsError, slc.slice_df, 'Little Saigon', 'any', 6)


    # Best practice for loops in unittests?
    def test_weekend_slicer_on_valid_neighborhoods(self):
        # Import the dataset
        filepath = os.path.join(os.path.dirname(__file__), "data/Annual_Parking_Study_Data_Cleaned2.csv")
        df = pd.read_csv(filepath, low_memory=False)

        # Neighborhoods that have data
        test_ballard = df.loc[(df['Neighborhood'] == 'Ballard') & (df['Weekday or weekend'] == 'weekend') & (df['Hour'] == 12)]
        test_chinatown = df.loc[(df['Neighborhood'] == 'Chinatown') & (df['Weekday or weekend'] == 'weekend') & (df['Hour'] == 12)]
        test_commercialcore = df.loc[(df['Neighborhood'] == 'Commercial Core') & (df['Weekday or weekend'] == 'weekend') & (df['Hour'] == 12)]
        test_greenlake = df.loc[(df['Neighborhood'] == 'Green Lake') & (df['Weekday or weekend'] == 'weekend') & (df['Hour'] == 12)]
        test_pioneersq = df.loc[(df['Neighborhood'] == 'Pioneer Square') & (df['Weekday or weekend'] == 'weekend') & (df['Hour'] == 12)]
        test_roosevelt = df.loc[(df['Neighborhood'] == 'Roosevelt') & (df['Weekday or weekend'] == 'weekend') & (df['Hour'] == 12)]
        test_uptown = df.loc[(df['Neighborhood'] == 'Uptown') & (df['Weekday or weekend'] == 'weekend') & (df['Hour'] == 12)]

        assert_frame_equal(test_ballard, slc.slice_df('Ballard', 'weekend', 12))
        assert_frame_equal(test_chinatown, slc.slice_df('Chinatown', 'weekend', 12))
        assert_frame_equal(test_commercialcore, slc.slice_df('Commercial Core', 'weekend', 12))
        assert_frame_equal(test_greenlake, slc.slice_df('Green Lake', 'weekend', 12))
        assert_frame_equal(test_pioneersq, slc.slice_df('Pioneer Square', 'weekend', 12))
        assert_frame_equal(test_roosevelt, slc.slice_df('Roosevelt', 'weekend', 12))
        assert_frame_equal(test_uptown, slc.slice_df('Uptown', 'weekend', 12))

    
    # Loops in unittests? How best to test this?
    def test_weekday_slicer_on_valid_neighborhoods(self):
        pass

if __name__ == "__main__":
    unittest.main()
