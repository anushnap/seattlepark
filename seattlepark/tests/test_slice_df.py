import unittest
import os
import pandas as pd
import seattlepark.slice_df as slc

class TestDataSlice(unittest.TestCase):

    def test_raises_Invalid_Area_Exception(self):
        self.assertRaises(slc.InvalidAreaError, slc.slice_df, 'Invalid neighborhood', 'any', 0)

    def test_raises_Invalid_DayType_Exception(self):
        self.assertRaises(slc.InvalidDayTypeError, slc.slice_df, 'Ballard', 'Monday', 0)

    def test_raises_No_Search_Results_Exception(self):
        pass


if __name__ == "__main__":
    unittest.main()
