# This class is to make sure the calculated distance and coordinates are connected to the same object.
# Everything in the class became one entity. If you sort the objects based on the values of one class member, then
# other class members will also be sorted accordingly.
# In this way, we can sort the list of the objects by the calculated distance
# and the coordinates will also be sorted accordingly.

# distance: the calculated distance between destination and this potential parking spot.
# coordinates: the coordinates of the start and end of this potential parking street.
#              e.x.: If the start and end coordinates of the street are (1,2) and (3,4), where 1 and 3 are latitude
#                    and 2 and 4 are longitude. Then the coordinates field will look like [[1,3], [2,4]]. This is the
#                    format which plotly uses to show a street on a map.
# street_name : the street address.
# street_lat_mid: the latitude of the middle point of this street.
# street_lon_mid: the longitude of the middle point of this street.
class ParkingSpot:
    def __init__(self, distance, coordinates, street_name, street_lat_mid, street_lon_mid, spaces_available):
        self.calculated_distance = distance
        self.street_meet_expect_coordinates = coordinates
        self.street_name = street_name
        self.street_lat_mid = street_lat_mid
        self.street_lon_mid = street_lon_mid
        self.spaceavail = 0


