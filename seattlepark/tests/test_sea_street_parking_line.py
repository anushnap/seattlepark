import unittest
from unittest.mock import Mock
from parking_spot import ParkingSpot
from sea_street_parking_line import create_parking_spots


class StreetParkingUITest(unittest.TestCase):

    def test_create_parking_spots_success(self):
        n_clicks = 1
        destination = "Street0"
        accept_distance = "0.2"
        layout = Mock()
        cu = Mock()

        distance = 0.5
        coordinates = [[1.1, 1.2], [1.3, 1.4]]
        street_name = "Street Name1"
        street_lat_mid = 1.5
        street_lon_mid = 1.6
        ps1 = ParkingSpot(distance, coordinates, street_name,
                          street_lat_mid, street_lon_mid)

        distance = 1.5
        coordinates = [[2.1, 2.2], [2.3, 2.4]]
        street_name = "Street Name2"
        street_lat_mid = 2.5
        street_lon_mid = 2.6
        ps2 = ParkingSpot(distance, coordinates, street_name,
                          street_lat_mid, street_lon_mid)

        spots = [ps1, ps2]
        destination_coordinates = [3.1, 3.2]

        cu.get_parking_spots.return_value = (spots, destination_coordinates)

        streets, notification = create_parking_spots(n_clicks, destination, accept_distance, layout, cu)

        data = streets["data"]
        lat1 = data[0]["lat"]
        lon1 = data[0]["lon"]
        self.assertEqual([lat1, lon1], [[1.1, 1.2], [1.3, 1.4]])

        lat2 = data[1]["lat"]
        lon2 = data[1]["lon"]
        self.assertEqual([lat2, lon2], [[2.1, 2.2], [2.3, 2.4]])

        lat3 = data[2]["lat"][0]
        lon3 = data[2]["lon"][0]
        self.assertEqual([lat3, lon3], [3.1, 3.2])

    def test_create_parking_spots_button_not_clicked(self):
        n_clicks = 0
        destination = "I love sushi seattle"
        accept_distance = "0.2"
        layout = Mock()
        cu = Mock()

        streets, notification = create_parking_spots(n_clicks, destination, accept_distance, layout, cu)
        data = streets["data"]
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        self.assertEqual([lat, lon], [[], []])

    def test_create_parking_spots_invalid_address(self):
        n_clicks = 1
        destination = "I love sushi seattle"
        accept_distance = "0.2"
        layout = Mock()
        cu = Mock()

        distance = 0.5
        coordinates = [[1.1, 1.2], [1.3, 1.4]]
        street_name = "Street Name1"
        street_lat_mid = 1.5
        street_lon_mid = 1.6
        ps1 = ParkingSpot(distance, coordinates, street_name,
                          street_lat_mid, street_lon_mid)

        distance = 1.5
        coordinates = [[2.1, 2.2], [2.3, 2.4]]
        street_name = "Street Name2"
        street_lat_mid = 2.5
        street_lon_mid = 2.6
        ps2 = ParkingSpot(distance, coordinates, street_name,
                          street_lat_mid, street_lon_mid)

        spots = [ps1, ps2]
        destination_coordinates = None

        cu.get_parking_spots.return_value = (spots, destination_coordinates)

        streets, notification = create_parking_spots(n_clicks, destination, accept_distance, layout, cu)

        data = streets["data"]
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        self.assertEqual([lat, lon], [[], []])

    def test_create_parking_spots_invalid_spots_returned(self):
        n_clicks = 1
        destination = "I love sushi seattle"
        accept_distance = "0.2"
        layout = Mock()
        cu = Mock()

        spots = None
        destination_coordinates = [3.1, 3.2]

        cu.get_parking_spots.return_value = (spots, destination_coordinates)

        streets, notification = create_parking_spots(n_clicks, destination, accept_distance, layout, cu)

        data = streets["data"]
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        self.assertEqual([lat, lon], [[], []])

    def test_create_parking_spots_no_spots_available(self):
        n_clicks = 1
        destination = "I love sushi seattle"
        accept_distance = "0.2"
        layout = Mock()
        cu = Mock()

        spots = []
        destination_coordinates = [3.1, 3.2]

        cu.get_parking_spots.return_value = (spots, destination_coordinates)

        streets, notification = create_parking_spots(n_clicks, destination, accept_distance, layout, cu)

        data = streets["data"]
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        self.assertEqual([lat, lon], [[], []])


if __name__ == "__main__":
    unittest.main()
