"""
I'm not actually sure if we need to do a unit test for a class where all it
has is an init that assigns the parameters. Just writing in a bunch of 
useless tests anyway
"""
import unittest
from seattlepark.src.parking_spot import ParkingSpot


class TestParkingSpotInit(unittest.TestCase):
    """ Test the ParkingSpot constructor"""
    def test_parking_spot(self):
        test_ps = ParkingSpot(
            1, [[1, 3], [2, 4]], 
            "1ST AVE BETWEEN SENECA ST AND UNIVERSITY ST",
            1, 1)
        
        self.assertEqual(test_ps.calculated_distance, 1)
        self.assertEqual(test_ps.street_meet_expect_coordinates,
                         [[1, 3], [2, 4]])
        self.assertEqual(test_ps.street_name, 
                         "1ST AVE BETWEEN SENECA ST AND UNIVERSITY ST")
        self.assertEqual(test_ps.street_lat_mid, 1)
        self.assertEqual(test_ps.street_lon_mid, 1)
        self.assertEqual(test_ps.spaceavail, 0)

    def test_parking_spot_raises_Exception(self):
        # Write test here about being passed empty street string?
        pass

if __name__ == "__main__":
    unittest.main()
