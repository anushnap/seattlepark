# slice_df.py
# this function imports the dataset, takes slice parameters, and returns a sliced dataframe
import pandas as pd
import numpy as np
import os

class InvalidAreaError(Exception):
    pass


class InvalidDayTypeError(Exception):
    pass


class NoSearchResultsError(Exception):
    pass


def slice_df(nhood, daytype, hour):
    # nhood: name of a neighborhood (might replace with lat/long later)
    # daytype: weekday, weekend, or any
    # hour: 0-23

    # check for valid inputs
    valid_neighborhoods = ['12th Ave', '15th Ave', 'Ballard', 'Belltown',
                           'Capitol Hill', 'Cherry Hill', 'Chinatown', 'Columbia City',
                           'Commercial Core', 'Denny Triangle', 'First Hill',
                           'Fremont', 'Green Lake', 'Lake City', 'Little Saigon',
                           'Pike-Pine', 'Pioneer Square', 'Roosevelt', 'SODO',
                           'South Lake Union', 'University District', 'Uptown',
                           'West Seattle', 'Westlake']
    valid_neighborhoods_lower = [i.lower() for i in valid_neighborhoods]

    nhood_in_list = False  # a flag to indicate if we found nhood in the valid inputs list
    # ensure nhood input is in the correct case
    for i, valid_neighborhood in enumerate(valid_neighborhoods_lower):
        # search through the lowercased valid list until you find a match
        if nhood.lower() == valid_neighborhood:
            # when match is found, replace nhood with the corresponding entry from the properly cased list
            nhood = valid_neighborhoods[i]
            nhood_in_list = True  # set flag to True
            break  # no point in continuing the loop once we found it

    # raise an exception if nhood was not found in the valid inputs list
    if not nhood_in_list:
        raise InvalidAreaError("The specified neighborhood is not recognized")

    valid_daytypes = ['weekday', 'weekend', 'any']
    if daytype.lower() not in valid_daytypes:
        raise InvalidDayTypeError("The specified day type is not recognized")


    filepath = os.path.join(os.path.dirname(__file__), "data/Annual_Parking_Study_Data_Cleaned2.csv")
    # Import the dataset
    df = pd.read_csv(filepath, low_memory=False)

    nhood_slicer = df['Neighborhood'] == nhood
    hour_slicer = df['Hour'] == hour

    if daytype == 'any':
        daytype_slicer = (df['Weekday or weekend'] == 'weekday') | (df['Weekday or weekend'] == 'weekend')
    else:
        daytype_slicer = df['Weekday or weekend'] == daytype.lower()

    df_sliced = df[nhood_slicer & daytype_slicer & hour_slicer]

    # check if resulting slice has anything in i
    if df_sliced.shape[0] == 0:
        raise NoSearchResultsError('The specified filter returned no data')
    else:
        return df_sliced
