# Class ParkingRecommender
# This class defines a ParkingRecommender object that is initialized with a
# list of ParkingSpot objects and a datetime (as a string), which are stored
# as class attributes.

# IMPORTANT NOTE!!!!
# This replaces the slice_df.py, max_freespace.py, and where_to_park.py
# modules! So don't use those anymore.

# The __init__ method is the constructor of the ParkingRecommender object
# and parses the datetime input and filters the full parking study dataset
# down to just the streets in the ParkingSpot list, using method slice_df().

# The max_freespace method uses that filtered dataset and returns the 5
# streets with the highest estimated parking availability, based on average
# observed availability from the parking study data.

# Use this method as follows:

# "ps" is a list of ParkingSpot objects (at least 5 entries)
# "dt" is a datetime string such as '2020-02-04 12:46:29.315237'
# pr = ParkingRecommender(ps,dt)
# output = pr.recommend()
# Here, output is a list of 5 ParkingSpot objects, with their .spaceavail
# attributes filled in.

import os
import numpy as np
import pandas as pd


class NoParkingSpotsInListError(Exception):
    pass


class NoSearchResultsError(Exception):
    pass


class InvalidStreetError(Exception):
    pass


class ParkingRecommender:
    def __init__(self, parkingspotlist, datetimestr):
        """
        parkingspotlist is a List object containing ParkingSpot objects, the
        output of the coordinates_util module.
        datetimestr is the user's requested date/time for parking data
        (computer time at time request is made?)
        """
        self.initial_list = parkingspotlist

        if len(self.initial_list) == 0:
            raise NoParkingSpotsInListError(
                'No streets were passed to the recommender'
            )

        datetime = pd.to_datetime(datetimestr)
        self.hr = datetime.hour

        self.initial_df = self.slice_by_street()

    def slice_by_street(self):
        """
        Import the Parking Study dataset and filter it down to the streets
        contained in parkingspotlist
        """
        # Extract street names from list of ParkingSpot objects
        street_names = []
        for st in self.initial_list:
            street_names.append(st.street_name)

        filepath = os.path.join(
                os.path.dirname(__file__),
                "../src/resources/Annual_Parking_Study_Data_Cleaned2.csv"
                )

        # Import the dataset
        df = pd.read_csv(filepath, low_memory=False)

        # check if all the requested street names are in the database
        unitdescs = df['Unitdesc'].unique()
        for name in street_names:
            if name not in unitdescs:
                raise InvalidStreetError(
                    'Street %s not found in Parking Study database' % name
                )

        df_sliced = df[df['Unitdesc'].isin(street_names)]
        return df_sliced

    def slice_by_hour(self, req_hr):
        """
        Slice initial_df to the requested hour, return further sliced df
        """
        # filter initial_df down to the requested hour
        df_this_hour = self.initial_df[
            self.initial_df['Hour'] == req_hr
        ]

        # check if there were any results
        if df_this_hour.shape[0] == 0:
            # no observations at specified hour, try one hour later
            # print('no results at %d' % req_hr)
            if req_hr < 23:
                new_hr = req_hr + 1
            else:  # there is no hour 24, wraps around to 0
                new_hr = 0
            # print('trying %d' % new_hr)
            df_this_hour = self.initial_df[
                self.initial_df['Hour'] == new_hr
            ]

        # check again to see if that worked
        if df_this_hour.shape[0] == 0:
            # still no observations, try one hour earlier
            # print('no results at %d' % new_hr)
            if req_hr > 0:
                new_hr = req_hr - 1
            else:  # there is no hour -1, wraps around to 23
                new_hr = 23
            # print('trying %d' % new_hr)
            df_this_hour = self.initial_df[
                self.initial_df['Hour'] == new_hr
            ]

        # check again to see if that worked
        if df_this_hour.shape[0] == 0:
            # still no observations, raise an error that we can catch
            # print('no results at %d' % new_hr)
            raise NoSearchResultsError
        else:
            return df_this_hour

    def max_freespace(self):
        """
        Return a tuple (streets,free_spaces) for all the streets
        in the initial list
        """
        # slice df to the requested hour
        df2 = self.slice_by_hour(self.hr)

        # List of unique streets in initial_df
        streets = df2['Unitdesc'].unique()

        # initialize a list to keep track of free spaces on each street
        free_spaces = np.zeros((len(streets),))
        # loop through each street and calculate free spaces
        for i, street in enumerate(streets):
            # filter the df to list observations from street (unitdesc) i only
            this_street = df2[df2['Unitdesc'] == street]

            # how many sides does this street have? At most 2
            sides = this_street['Side'].unique()

            for side in sides:
                # filter to just this side
                this_side = this_street[this_street['Side'] == side]
                num_obs = this_side.shape[0]
                if num_obs > 0:
                    # This calculation gives "free spaces per observation,"
                    # an estimate of how many spaces are available
                    avg_freespace = this_side['Free_Spaces'].mean()
                    free_spaces[i] += avg_freespace

        return streets, free_spaces

    def recommend(self, num_returns=5):
        """
        Returns a num_returns-length list of parking spots
        with the highest estimated number of available spaces
        """
        try:
            (streets, free_spaces) = self.max_freespace()
        except NoSearchResultsError:

            # no observations in self.hr +/- 1
            # just return the num_returns closest streets
            newlist = sorted(self.initial_list,
                             key=lambda x: x.calculated_distance,
                             reverse=False)
            n_entries = min(len(self.initial_list), num_returns)
            # print('Returning %d closest spots' % n_entries)
            # for i in range(n_entries):
            #     print(newlist[i].street_name)
            return newlist[0:n_entries]

        # Assuming no exception was raised:
        sort_index = np.argsort(free_spaces)
        free_spaces_sorted = free_spaces[sort_index]
        streets_sorted = streets[sort_index]
        # The sort is in ascending order, so take the last num_returns entries
        n_entries = min(len(streets), num_returns)
        streets_select = streets_sorted[-n_entries:]
        free_spaces_select = free_spaces_sorted[-n_entries:]

        # Now, downselect the list of ParkingSpots to just the ones selected
        output_list = []
        for i, select in enumerate(streets_select):
            #  find "select" in self.initial_list
            for j in range(len(self.initial_list)):
                if self.initial_list[j].street_name == select:
                    # Fill in the .spaceavail attribute
                    self.initial_list[j].spaceavail = free_spaces_select[i]

                    # Copy this entry over to the output list
                    output_list.append(self.initial_list[j])
                    break  # don't continue searching for "select" after found

        # # some debugging print statements
        # for i in range(len(output_list)):
        #     print('%s: %4.1f spaces' % (
        #         output_list[i].street_name,
        #         output_list[i].spaceavail
        #     )
        #           )

        return output_list
