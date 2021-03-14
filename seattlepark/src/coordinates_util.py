import json
import os
import sys

from geopy import GoogleV3
import haversine as hs

from parking_recommender import ParkingRecommender
from parking_spot import ParkingSpot
import base64
import datetime


class CoordinatesUtil:
    """
    This class is used to provide the parking spots to the user.

    Attributes
    ----------
    coordinates_mapping: dictionary
        a dictionary with the key as street name, and value is a list of
        1) a list of coordinates of start and end of a street
        2) mid-point of a street
    geo_locator: Instance of GoogleV3
        GoogleV3 is a class of library geopy. It helps to get the coordinates of the user input destination address.

    Methods
    -------
    sea_parking_geocode()
        Load the json file and return the coordinates_mapping.

    get_parking_spots(destination_address, acceptable_distance)
        Return the top 5 recommended parking spots and the coordinates of the user input destination address.

    get_destination_coordinates(destination_address)
        Using Google Map API to return the coordinates of the user input destination address.

    cal_distance(coordinates1, coordinates2)
        Calculate the distance between the user input destination and each parking street.
        Return the calculated distance.

    decode_data(file_location)
        Decode the required base64 encoded data.
    """

    coordinates_mapping = {}

    def __init__(self):
        key = self.decode_data('resources/google_map_api.key')
        # Initializing the geo location to the GoogleV3 in the constructor
        #   with the google api key extracted above
        self.geo_locator = GoogleV3(api_key=key)
        self.sea_parking_geocode()

    def sea_parking_geocode(self):
        """
        Load the json file and return the coordinates_mapping.
        """
        if self.coordinates_mapping and len(
                self.coordinates_mapping) > 0:
            return self.coordinates_mapping
        else:
            path = os.path.join(os.path.dirname(__file__),
                                'resources/Midpoints_and_LineCoords.json')
            with open(path) as json_data:
                seattle_data = json.load(json_data)
                features = seattle_data["features"]
                for feature in features:
                    properties = feature["properties"]
                    geometry = feature["geometry"]
                    coordinates = geometry["coordinates"]
                    mid_point = geometry["midpoint"]
                    address = properties["UNITDESC"]
                    lat_start = coordinates[0][1]
                    lat_end = coordinates[1][1]
                    log_start = coordinates[0][0]
                    log_end = coordinates[1][0]
                    line_latitudes = [lat_start, lat_end]
                    line_longitudes = [log_start, log_end]
                    dot_mid_street_lat = mid_point[1]
                    dot_mid_street_log = mid_point[0]
                    self.coordinates_mapping[address] = \
                        [[line_latitudes, line_longitudes],
                         [dot_mid_street_lat, dot_mid_street_log]]

    def get_parking_spots(self, destination_address, acceptable_distance):
        """
        Return the top 5 recommended parking spots and the coordinates of the user input destination address.

        Parameters
        ----------
        destination_address: str, required
            User input destination address

        acceptable_distance: int or float, required
            User input acceptable walking distance from the destination address.

        Returns
        -------
        Tuple
            if an Exception occurs when the user input destination is invalid or the ParkingRecommender class doesn't
            return any recommended parking spot;
            or if all calculated distance between the destination address and each parking street is greater than
            the acceptable walking distance entered by the user,
            then return a tuple of empty list and None.

            Otherwise, return the top 5 recommended parking spots and the coordinates of the user input destination
            address.
        """

        distance = float(acceptable_distance)

        try:
            destination_coordinates = self.get_destination_coordinates(destination_address)
            print(f"Destination Coordinates: {destination_coordinates}")
        except Exception:
            print(f"Invalid Destination: {destination_address}")
            return [], None

        street_meet_expect = []
        for street in self.sea_parking_geocode():
            street_mid_coordinates = self.coordinates_mapping[street][1]
            street_start_and_end_coordinates = \
                self.coordinates_mapping[street][0]

            distance_in_between = self.cal_distance(
                destination_coordinates, street_mid_coordinates)

            if distance_in_between <= distance:
                ps = ParkingSpot(
                    distance_in_between,
                    street_start_and_end_coordinates,
                    street,
                    street_mid_coordinates[0],
                    street_mid_coordinates[1])
                street_meet_expect.append(ps)

        if len(street_meet_expect) == 0:
            return [], None
        else:
            current_utc_time = datetime.datetime.now()
            pr = ParkingRecommender(street_meet_expect, current_utc_time)
            try:
                recommended_spots = pr.recommend()
                return recommended_spots, destination_coordinates
            except Exception:
                return street_meet_expect[0:5], destination_coordinates

    def get_destination_coordinates(self, destination_address):
        """
        Using Google Map API to return the coordinates of the user input destination address.

        Parameters
        ----------
        destination_address: str, required
            User input destination address.

        Returns
        -------
        list
            a list of the latitude and longitude of the user input destination address.
        """
        coordinates = self.geo_locator.geocode(destination_address)
        return [coordinates.latitude, coordinates.longitude]

    def cal_distance(self, coordinates1, coordinates2):
        """
        Calculate the distance between the user input destination and each parking street.
        Return the calculated distance.

        Parameters
        ----------
        coordinates1: list, required
            a list of latitude and longitude

        coordinates2: list, required
            a list of latitude and longitude

        Returns
        -------
        float
            if an Exception occurs, return the system max size as calculated distance
            between coordinates1 and coordinates2.

            otherwise, return the distance between coordinates1 and coordinates2 in miles.
        """
        try:
            calculated_distance = hs.haversine(coordinates1, coordinates2, unit="mi")
        except Exception:
            return sys.maxsize  # In case of exception in calculating the distance between two coordinates, default the
            # calculated distance to max size to filter the coordinate out.
        return calculated_distance

    def decode_data(self, file_location):
        """
        Decode the required base64 encoded data.

        Parameters
        ----------
        file_location: str, required
            the location of the file.

        Returns
        -------
        str
            decoded string of the input base64 decoded string.
        """
        path = os.path.join(os.path.dirname(__file__), file_location)
        with open(path) as handle:
            encoded_key_str = handle.read()
            # make str into bytes, for encoding and decoding
            encoded_bytes = encoded_key_str.encode("ascii")
            decoded_bytes = base64.b64decode(encoded_bytes)
            return decoded_bytes.decode("ascii")
