class ParkingSpot:
    """
    This class represents a parking spot on the map.

    Attributes
    ----------
    distance: float
        the calculated distance between destination and this potential
        parking spot.

    coordinates: list
        the coordinates of the start and end of this potential parking street.

    street_name: str
        the street address.

    street_lat_mid: float
        the latitude of the middle point of this street.

    street_lon_mid: float
        the longitude of the middle point of this street.

    spaceavail: integer
        provide the number of spaces that are available in a parking street.

    """
    def __init__(self, distance, coordinates, street_name,
                 street_lat_mid, street_lon_mid):
        """
        Parameters
        ----------
        distance: float
            the calculated distance between destination and this potential
            parking spot.

        coordinates: list
            the coordinates of the start and end of this potential parking
            street.

        street_name: str
            the street address.

        street_lat_mid: float
            the latitude of the middle point of this street.

        street_lon_mid: float
            the longitude of the middle point of this street.
        """
        self.calculated_distance = distance
        self.street_meet_expect_coordinates = coordinates
        self.street_name = street_name
        self.street_lat_mid = street_lat_mid
        self.street_lon_mid = street_lon_mid
        self.spaceavail = 0
