# import pandas as pd
# from statistics import mean

import plotly
import plotly.express as px


class Histogram:
    def __init__(self, data):
        """Constructor for Histogram object. Takes a dataframe as input."""

        # Note:
        # I refactored the ParkingRecommender class and now it stores
        # a filtered parking study dataframe with just the 20 streets
        # passed in by CoordinatesUtil. So that will be faster to work
        # with than the entire dataset of 1.3k streets.
        # I plan to create a Histogram object inside of a ParkingRecommender
        # method, so I can just pass that dataframe to the constructor.
        # - Patrick, 3-4-21 10:06 PM

        # Subset dataframe with just:
        # Unitdesc, Day of week, Hour,
        # Parking_Spaces, Utilization, Free_Spaces
        # Note on Day of week: Monday = 1, Sunday = 7
        # subset_data = data[["Unitdesc", "Hour","Day of week",
        # "Parking_Spaces", "Total_Vehicle_Count",
        # "Utilization", "Free_Spaces"]]

        subset_data = data[["Unitdesc", "Hour", "Free_Spaces"]]

        # Group data by unit and hour and get the
        # average number of free spaces
        self.average_free_spaces_df = \
            subset_data.groupby(["Unitdesc", "Hour"]).mean()

        # Reset indices
        self.average_free_spaces_df.reset_index(inplace=True)

        # Rename Free_Spaces column to Average_Free_Spaces
        self.average_free_spaces_df.columns = \
            ['Unitdesc', 'Hour', 'Average_Free_Spaces']

    # Note since data is already binned by hour, we're just creating bar chart
    def createHistogram(self, unit_name):
        # Create filtered dataframe based on unit_name
        filtered_data = self.average_free_spaces_df[
            self.average_free_spaces_df.Unitdesc == unit_name
        ]

        # Create histogram
        fig = px.bar(filtered_data, x='Hour', y='Average_Free_Spaces')
        # return "<html><head>Hourly Availability</head><body>" +
        # plotly.offline.plot(fig, output_type="div") + "</body></html>"
        return plotly.offline.plot(fig, output_type="div")

# if __name__ == '__main__':
#     hs = Histogram()
#     bar = hs.createHistogram("10TH AVE BETWEEN E MADISON ST AND E SENECA ST")
#     print(bar)
