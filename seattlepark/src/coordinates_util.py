import json
import os

from geopy import GoogleV3
import haversine as hs

from parking_recommender import ParkingRecommender
from parking_spot import ParkingSpot
import base64
import datetime


class CoordinatesUtil:
    coordinates_mapping = {}

    def __init__(self):
        key = self.decode_data('resources/google_map_api.key')
        # Initializing the geo location to the GoogleV3 in the constructor with the google api key extracted above
        self.geo_locator = GoogleV3(api_key=key)

    def sea_parking_geocode(self):
        if self.coordinates_mapping and len(
                self.coordinates_mapping) > 0:
            return self.coordinates_mapping
        else:
            path = os.path.join(os.path.dirname(__file__), 'resources/Midpoints_and_LineCoords.json')
            with open(path) as json_data:
                seattle_data = json.load(json_data)
                features = seattle_data["features"]
                for feature in features:
                    properties = feature["properties"]
                    geometry = feature["geometry"]
                    coordinates = geometry["coordinates"]
                    mid_point = geometry["midpoint"]
                    address = properties["UNITDESC"]  # How about using geo_locator.geocode.reverse()???
                    lat_start = coordinates[0][1]
                    lat_end = coordinates[1][1]
                    log_start = coordinates[0][0]
                    log_end = coordinates[1][0]
                    line_latitudes = [lat_start, lat_end]
                    line_longitudes = [log_start, log_end]
                    dot_mid_street_lat = mid_point[1]
                    dot_mid_street_log = mid_point[0]
                    self.coordinates_mapping[address] = [[line_latitudes, line_longitudes],
                                                         [dot_mid_street_lat, dot_mid_street_log]]

            return self.coordinates_mapping  # {"address" : [ [line_latitudes, line_longitudes], [dot_lat, dot_log] ]}

    def get_parking_spots(self, destination_address, acceptable_distance):
        # return the coordinate of the user destination
        distance = float(acceptable_distance)
        destination_coordinates = self.get_destination_coordinates(destination_address)
        street_meet_expect = []
        for street in self.sea_parking_geocode():
            street_mid_coordinates = self.coordinates_mapping[street][1]
            street_start_and_end_coordinates = self.coordinates_mapping[street][0]

            distance_in_between = self.cal_distance(destination_coordinates, street_mid_coordinates)

            if distance_in_between <= distance:
                ps = ParkingSpot(distance_in_between, street_start_and_end_coordinates, street,
                                 street_mid_coordinates[0], street_mid_coordinates[1])
                street_meet_expect.append(ps)

        if len(street_meet_expect) == 0:
            return [], None
        else:
            # street_meet_expect.sort(key=lambda point: point.calculated_distance)
            current_utc_time = datetime.datetime.now()
            pr = ParkingRecommender(street_meet_expect, current_utc_time)
            try:
                recommended_spots = pr.recommend()
                return recommended_spots, destination_coordinates
            except Exception:
                return street_meet_expect[0:5], destination_coordinates

    def get_destination_coordinates(self, destination_address):
        coordinates = self.geo_locator.geocode(destination_address)
        print(coordinates)
        return [coordinates.latitude, coordinates.longitude]

    def cal_distance(self, coordinates1, coordinate2):
        # return the distance between coordinates1 and coordinates2
        calculated_distance = hs.haversine(coordinates1, coordinate2, unit="mi")
        return calculated_distance

    def decode_data(self, file_location):
        path = os.path.join(os.path.dirname(__file__), file_location)
        with open(path) as handle:
            encoded_key_str = handle.read()
            encoded_bytes = encoded_key_str.encode("ascii")  # make str into bytes, for encoding and decoding
            decoded_bytes = base64.b64decode(encoded_bytes)
            return decoded_bytes.decode("ascii")
