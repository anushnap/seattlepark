import pandas as pd
from statistics import mean

import plotly
import plotly.express as px


class Histogram:
    def __init__(self):
        # Read in data
        data = pd.read_csv("resources/Annual_Parking_Study_Data_Cleaned2.csv", low_memory=False)

        # Subset dataframe with just Unitdesc, Day of week, Hour, Parking_Spaces, Utilization, Free_Spaces
        # Note on Day of week: Monday = 1, Sunday = 7
        # subset_data = data[["Unitdesc", "Hour","Day of week", "Parking_Spaces", "Total_Vehicle_Count", "Utilization", "Free_Spaces"]]

        subset_data = data[["Unitdesc", "Hour", "Free_Spaces"]]

        # Group data by unit and hour and get the average number of free spaces
        self.average_free_spaces_df = subset_data.groupby(["Unitdesc", "Hour"]).mean()

        # Reset indices
        self.average_free_spaces_df.reset_index(inplace=True)

        # Rename Free_Spaces column to Average_Free_Spaces
        self.average_free_spaces_df.columns = ['Unitdesc', 'Hour', 'Average_Free_Spaces']

    # Note since data is already binned by hour, we're just creating bar chart
    def createHistogram(self, unit_name):
        # Create filtered dataframe based on unit_name
        filtered_data = self.average_free_spaces_df[self.average_free_spaces_df.Unitdesc == unit_name]

        # Create histogram
        fig = px.bar(filtered_data, x='Hour', y='Average_Free_Spaces')
        # return "<html><head>Hourly Availability</head><body>" + plotly.offline.plot(fig, output_type="div") + "</body></html>"
        return plotly.offline.plot(fig, output_type="div")

# if __name__ == '__main__':
#     hs = Histogram()
#     bar = hs.createHistogram("10TH AVE BETWEEN E MADISON ST AND E SENECA ST")
#     print(bar)