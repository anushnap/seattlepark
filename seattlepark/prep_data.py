# Set up data cleaning process
import os
import pandas as pd

# Create new exception
class MissingStudyArea(Exception):
    pass


# Split Study_Area on - character and create separate columns
def clean_area_col(parking):
    
    if('Study_Area' not in parking.columns):
        raise MissingStudyArea("Data is missing Study_Area column")
    else:
        areas = parking['Study_Area'].str.split('-', expand = True)
        parking['Area'] = areas[0].str.strip()
        parking['Sub-Area'] = areas[1].str.strip() + ' - ' + areas[2].str.strip()


if __name__ == "__main__":
    wd = os.getcwd()

    # Fix dtypeWarning error (22, 23) have mixed types
    parking = pd.read_csv(wd + "/data/Annual_Parking_Study_Data.csv")
    clean_area_col(parking)