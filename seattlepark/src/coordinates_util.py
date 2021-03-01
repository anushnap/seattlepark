import json
from geopy import GoogleV3
import haversine as hs
from parking_spot import ParkingSpot
import base64

class CoordinatesUtil:
    coordinates_mapping = {}
    neighboring_streets_count = 20

    def __init__(self):
        with open("resources/google_map_api.key") as handle:
            encoded_key_str = handle.read()
            encoded_bytes = encoded_key_str.encode("ascii")  # make str into bytes, for encoding and decoding
            decoded_bytes = base64.b64decode(encoded_bytes)
            self.key = decoded_bytes.decode("ascii")

    def sea_parking_geocode(self):
        if self.coordinates_mapping and len(
                self.coordinates_mapping) > 0:
            return self.coordinates_mapping
        else:
            with open(
                    'resources/Midpoints_and_LineCoords.json') as json_data:
                seattle_data = json.load(json_data)
                features = seattle_data["features"]
                for feature in features:
                    properties = feature["properties"]
                    geometry = feature["geometry"]
                    coordinates = geometry["coordinates"]
                    mid_point = geometry["midpoint"]
                    address = properties["UNITDESC"].title() # How about using geo_locator.geocode.reverse()???
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
        destination_coordinates = self.get_destination_coordinates(destination_address)

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
            return []
        else:
            street_meet_expect.sort(key=lambda point: point.calculated_distance)
            top_spots = street_meet_expect[0:self.neighboring_streets_count]
            return top_spots

    def get_destination_coordinates(self, destination_address):
        geo_locator = GoogleV3(api_key=self.key)
        coordinates = geo_locator.geocode(destination_address).point
        print(coordinates)
        return [coordinates.latitude, coordinates.longitude]

    def cal_distance(self, coordinates1, coordinate2):
        # return the distance between coordinates1 and coordinates2
        calculated_distance = hs.haversine(coordinates1, coordinate2, unit="mi")
        return calculated_distance

