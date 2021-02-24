# This class is to make sure the calculated distance and coordinates are connected to the same object.
# Everything in the class became one entity. If you sort the objects based on the values of one class member, then
# other class members will also be sorted accordingly.
# In this way, we can sort the list of the objects by the calculated distance
# and the coordinates will also be sorted accordingly.

class ParkingSpot:
    def __init__(self, distance, coordinates, street_name, street_lat_mid, street_lon_mid):
        self.calculated_distance = distance
        self.street_meet_expect_coordinates = coordinates
        self.street_name = street_name
        self.street_lat_mid = street_lat_mid
        self.street_lon_mid = street_lon_mid


