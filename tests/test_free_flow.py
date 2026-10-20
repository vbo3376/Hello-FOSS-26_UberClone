"""Per-vehicle, per-class free-flow speeds (issue 001, step 1)."""
import unittest

from routing import AUTO, BIKE, CAR, RoadClass
from routing.models import EdgeMeta, free_flow_speed_kmh
from routing.vehicles import SPEED_BREAKER_FACTOR


class FreeFlowSpeedTests(unittest.TestCase):
    def test_class_speed_when_no_limit(self):
        self.assertEqual(free_flow_speed_kmh(RoadClass.RESIDENTIAL, None, CAR), CAR.free_flow_kmh[RoadClass.RESIDENTIAL])
        self.assertGreater(free_flow_speed_kmh(RoadClass.PRIMARY, None, CAR),
                           free_flow_speed_kmh(RoadClass.RESIDENTIAL, None, CAR))

    def test_legal_limit_caps_the_class_speed(self):
        self.assertEqual(free_flow_speed_kmh(RoadClass.PRIMARY, 20.0, CAR), 20.0)          # school zone
        self.assertEqual(free_flow_speed_kmh(RoadClass.PRIMARY, 100.0, CAR), CAR.free_flow_kmh[RoadClass.PRIMARY])

    def test_speed_breaker_applied_once(self):
        plain = free_flow_speed_kmh(RoadClass.PRIMARY, None, CAR)
        self.assertAlmostEqual(free_flow_speed_kmh(RoadClass.PRIMARY, None, CAR, True), plain * SPEED_BREAKER_FACTOR)

    def test_vehicles_differ(self):
        self.assertLess(free_flow_speed_kmh(RoadClass.TRUNK, None, AUTO), free_flow_speed_kmh(RoadClass.TRUNK, None, CAR))
        car, bike = (free_flow_speed_kmh(RoadClass.RESIDENTIAL, None, p) for p in (CAR, BIKE))
        self.assertLessEqual(abs(car - bike) / car, 0.1)       # bikes lose little on minor roads

    def test_profile_covers_every_road_class(self):
        for profile in (CAR, AUTO, BIKE):
            self.assertEqual(set(profile.free_flow_kmh), set(RoadClass), profile.vehicle)


if __name__ == "__main__":
    unittest.main()