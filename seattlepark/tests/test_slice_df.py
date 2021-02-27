import unittest
import os
import pandas as pd
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
        self.assertRaises(slc.NoSearchResultsError, slc.slice_df, '12th Ave', 'any', 4)
        self.assertRaises(slc.NoSearchResultsError, slc.slice_df, '12th Ave', 'any', 5)
        self.assertRaises(slc.NoSearchResultsError, slc.slice_df, '12th Ave', 'any', 6)


if __name__ == "__main__":
    unittest.main()
