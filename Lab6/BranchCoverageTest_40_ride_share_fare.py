import pytest

from ride_share_fare import extra_distance_fare, pickup_status, seats_and_bags_ok


def test_fare_validation_branches():
    with pytest.raises(ValueError, match="unknown cab type"):
        extra_distance_fare("luxury", 1, "city", False)
    with pytest.raises(ValueError, match="invalid distance"):
        extra_distance_fare("mini", -1, "city", False)


def test_fare_branches():
    # Subscriber adjustment: false, true for a non-SUV, and true for an SUV.
    assert extra_distance_fare("sedan", 5, "city", False) == 0
    assert extra_distance_fare("mini", 10, "city", True) == 24
    assert extra_distance_fare("suv", 20, "city", True) == 96

    # No extra distance, city/outstation rates, and the long-distance surcharge.
    assert extra_distance_fare("suv", 12, "city", False) == 0
    assert extra_distance_fare("sedan", 10, "city", False) == 24
    assert extra_distance_fare("sedan", 10, "outstation", False) == 36
    assert extra_distance_fare("mini", 30, "city", False) == 500
    assert extra_distance_fare("mini", 30, "outstation", False) == 750


def test_seat_and_bag_branches():
    assert seats_and_bags_ok(2, 10, True) is True
    assert seats_and_bags_ok(3, 0, True) is False
    assert seats_and_bags_ok(4, 2, False) is True
    assert seats_and_bags_ok(5, 0, False) is False
    assert seats_and_bags_ok(2, 3, False) is False


def test_pickup_status_branches():
    assert pickup_status(20, True, True) == "on_time"
    assert pickup_status(0, True, False) == "delayed"
    assert pickup_status(-11, False, False) == "missed"
