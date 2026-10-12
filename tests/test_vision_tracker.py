"""Unit tests for the gesture detection logic."""
import math
from types import SimpleNamespace

from backend.vision_tracker import VisionTracker


def test_distance_calculation():
    p1 = SimpleNamespace(x=0.0, y=0.0, z=0.0)
    p2 = SimpleNamespace(x=3.0, y=4.0, z=0.0)
    assert math.isclose(VisionTracker._distance(p1, p2), 5.0)


def test_tracker_instantiation():
    t = VisionTracker()
    assert t.gesture_state == "idle"
    assert t.prev_x is None