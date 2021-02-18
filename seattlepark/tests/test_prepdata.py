import unittest
import os
import pandas as pd
import prep_data as prd

class TestFilePrep(unittest.TestCase):

    def test_raises_Missing_Study_Area(self):
        filepath = os.getcwd()

        data = pd.read_csv(filepath + "/data/Annual_Parking_Study_Data.csv")
        missing_col = data.drop('Study_Area', axis = 1)

        self.assertRaises(prd.MissingStudyArea, prd.clean_area_col, missing_col)


if __name__ == "__main__":
    unittest.main()