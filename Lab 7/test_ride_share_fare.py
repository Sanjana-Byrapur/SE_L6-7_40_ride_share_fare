import math

import pytest
from hypothesis import given, strategies as st

from ride_share_fare import fare_average, parse_trip, payable_fare


@given(st.text() | st.none())
def test_parse_trip_no_crash(value):
    result = parse_trip(value)
    if result is not None:
        cab, distance = result
        assert cab and cab == cab.strip().title()
        assert math.isfinite(distance) and distance >= 0


@given(st.text() | st.none())
def test_fare_average_no_crash(value):
    result = fare_average(value)
    assert result is None or (isinstance(result, int) and result >= 0)


@given(st.text() | st.none())
def test_payable_fare_no_crash(value):
    result = payable_fare(value)
    assert result is None or (math.isfinite(result) and result >= 0)


@given(st.sampled_from(["mini", "sedan", "suv"]),
       st.floats(min_value=0, max_value=1e9, allow_nan=False, allow_infinity=False))
def test_parse_trip_valid(cab, distance):
    assert parse_trip(f" {cab} :{distance}") == (cab.title(), distance)


@given(st.lists(st.integers(min_value=0, max_value=10**9), min_size=1, max_size=30))
def test_fare_average_valid(fares):
    assert fare_average(",".join(map(str, fares))) == sum(fares) // len(fares)


@given(st.floats(min_value=0, max_value=1e9, allow_nan=False, allow_infinity=False),
       st.floats(min_value=0, max_value=1e9, allow_nan=False, allow_infinity=False))
def test_payable_fare_valid(fare, promo):
    assert payable_fare(f"{fare}|{promo}") == max(fare * 1.18 - promo, 0)


@pytest.mark.parametrize("value", ["", ":1", "mini:", "mini:-1", "mini:nan",
                                   "mini:inf", "mini:1:2", 42, [], {}])
def test_parse_trip_invalid(value):
    assert parse_trip(value) is None


@pytest.mark.parametrize("value", ["", ",", "1,,2", "1,-2", "1,2.5",
                                   pytest.param("9" * 5000, id="oversized_integer"),
                                   42, [], {}])
def test_fare_average_invalid(value):
    assert fare_average(value) is None


@pytest.mark.parametrize("value", ["", "1|", "|1", "1|2|3", "-1|0",
                                   "1|-1", "nan|1", "inf|1", "1.7e308|0",
                                   42, [], {}])
def test_payable_fare_invalid(value):
    assert payable_fare(value) is None
