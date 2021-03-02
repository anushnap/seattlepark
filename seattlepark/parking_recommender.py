# Class ParkingRecommender
# This class defines a ParkingRecommender object that is initialized with a list of ParkingSpot objects and a datetime
# (as a string), which are stored as class attributes.

# IMPORTANT NOTE!!!!
# This replaces the slice_df.py, max_freespace.py, and where_to_park.py modules! So don't use those anymore.

# The __init__ method is the constructor of the ParkingRecommender object and parses the datetime input and filters
# the full parking study dataset down to just the streets in the ParkingSpot list, using method slice_df().

# The max_freespace method uses that filtered dataset and returns the 5 streets with the highest estimated parking
# availability, based on average observed availability from the parking study data.

# Use this method as follows:

# "ps" is a list of ParkingSpot objects (at least 5 entries)
# "dt" is a datetime string such as '2020-02-04 12:46:29.315237'
# pr = ParkingRecommender(ps,dt)
# output = pr.max_freespace()
# Here, output is a list of 5 ParkingSpot objects, with their .spaceavail attributes filled in.


import numpy as np
import pandas as pd
import os


class NoSearchResultsError(Exception):
    pass


class InvalidStreetError(Exception):
    pass


class ParkingRecommender:
    def __init__(self, parkingspotlist, datetimestr):
        # parkingspotlist is a List object containing ParkingSpot objects, the output of the coordinates_util module.
        # datetimestr is the user's requested date/time for parking data (computer time at time request is made?)
        self.initial_list = parkingspotlist

        # extract weekday and hour from datetimestr and store them as object attributes
        datetime = pd.to_datetime(datetimestr)
        self.hr = datetime.hour
        # debugging print statement
        # print('Detected Hour: %d' % self.hr)
        # self.wkday = datetime.dayofweek

        # Run the slice_df function to filter the database immediately
        self.initial_df = self.slice_df()  # dataframe corresponding to the spots in initial_list

    def slice_df(self):
        """Import the Parking Study dataset and filter it down to the streets contained in parkingspotlist"""
        filepath = os.path.join(os.path.dirname(__file__), "data/Annual_Parking_Study_Data_Cleaned2.csv")
        # Import the dataset
        df = pd.read_csv(filepath, low_memory=False)

        # Extract street names from list of ParkingSpot objects
        street_names = []
        for st in self.initial_list:
            street_names.append(st.street_name)

        # check if all the requested street names are in the database
        unitdescs = df['Unitdesc'].unique()  # list of unique streets in database
        for name in street_names:
            if name not in unitdescs:
                raise InvalidStreetError('Street %s not found in Parking Study database' % name)

        df_sliced = df[df['Unitdesc'].isin(street_names) & (df['Hour'] == self.hr)]

        # check if resulting slice has anything in it
        if df_sliced.shape[0] == 0:
            raise NoSearchResultsError('The specified filter returned no data')
        else:
            return df_sliced

    def max_freespace(self):
        """Returns the 5 parking spots with the highest estimated number of available spaces"""
        # List of unique streets in initial_df
        streets = self.initial_df['Unitdesc'].unique()
        # initialize a list to keep track of free spaces on each street
        free_spaces = np.zeros((len(streets),))
        # loop through each street and calculate free spaces
        for i, street in enumerate(streets):
            # filter the df to list observations from street (unitdesc) i only
            this_street = self.initial_df[self.initial_df['Unitdesc'] == street]

            # how many sides does this street have? At most 2
            sides = this_street['Side'].unique()

            for side in sides:
                # filter to just this side
                this_side = this_street[this_street['Side'] == side]
                num_obs = this_side.shape[0]
                # This calculation gives "free spaces per observation," an estimate of how many spaces are available
                avg_freespace = this_side['Free_Spaces'].sum() / num_obs
                # debugging print
                # print('%s side of %s has %d obs and avg %4.1f spaces' % (side, street, num_obs, avg_freespace))
                # Add the average free spaces on this side to free_spaces
                # Eventually free_spaces[i] will have the total number of free spaces, on both sides of the street
                free_spaces[i] += avg_freespace

        # Now we have a list of streets, with a corresponding list of the estimated number of available spaces
        # Sort the list of freespaces and return the sorted index, so we can also sort the list of streets
        sort_index = np.argsort(free_spaces)
        free_spaces_sorted = free_spaces[sort_index]
        streets_sorted = streets[sort_index]
        # The sort is in ascending order, so take the last 5 entries.
        n_entries = -5
        streets_select = streets_sorted[n_entries:]
        free_spaces_select = free_spaces_sorted[n_entries:]

        # Now, downselect the list of ParkingSpots to just the the ones we've selected
        output_list = []
        for i, select in enumerate(streets_select):
            #  find "select" in self.initial_list
            for j in range(len(self.initial_list)):
                if self.initial_list[j].street_name == select:
                    # Fill in the .spaceavail attribute
                    self.initial_list[j].spaceavail = free_spaces_select[i]
                    # Copy this entry over to the output list
                    output_list.append(self.initial_list[j])
                    break  # no need to continue searching for "select" after finding it

        # some debugging print statements
        # for i in range(len(output_list)):
        #     print('%s: %4.1f spaces' % (output_list[i].street_name, output_list[i].spaceavail))

        return output_list
