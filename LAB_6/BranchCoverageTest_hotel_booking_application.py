
import pytest

from hotel_booking import (
    booking_cost,
    cancellation_refund,
    room_upgrade
)


# BOOKING COST - ALL DECISION BRANCHES

def test_invalid_room():
    with pytest.raises(ValueError):
        booking_cost("premium", 2, 2, False)


def test_zero_nights():
    with pytest.raises(ValueError):
        booking_cost("standard", 0, 2, False)


def test_negative_nights():
    with pytest.raises(ValueError):
        booking_cost("standard", -1, 2, False)


def test_peak_season_true():
    assert booking_cost("standard", 2, 2, True) == 5000


def test_peak_season_false():
    assert booking_cost("standard", 2, 2, False) == 4000


def test_more_than_two_guests():
    assert booking_cost("standard", 2, 3, False) == 5000


def test_exactly_two_guests():
    assert booking_cost("standard", 2, 2, False) == 4000


def test_one_guest():
    assert booking_cost("standard", 2, 1, False) == 4000


def test_seven_nights():
    assert booking_cost("standard", 7, 2, False) == 12600


def test_less_than_seven_nights():
    assert booking_cost("standard", 6, 2, False) == 12000


# CANCELLATION REFUND - ALL DECISION BRANCHES

def test_days_at_least_seven():
    assert cancellation_refund(1000, 7, False) == 1000


def test_days_between_two_and_six():
    assert cancellation_refund(1000, 5, False) == 500


def test_days_less_than_two():
    assert cancellation_refund(1000, 1, False) == 0


def test_member_gets_extra_refund():
    assert cancellation_refund(1000, 3, True) == 750


def test_non_member_refund():
    assert cancellation_refund(1000, 3, False) == 500


def test_member_early_cancellation():
    assert cancellation_refund(1000, 1, True) == 250


# ROOM UPGRADE - ALL DECISION BRANCHES

def test_no_rooms_available():
    assert room_upgrade("standard", True, 0) == "standard"


def test_rooms_available():
    assert room_upgrade("standard", True, 2) == "deluxe"


def test_standard_member():
    assert room_upgrade("standard", True, 1) == "deluxe"


def test_standard_non_member():
    assert room_upgrade("standard", False, 1) == "standard"


def test_deluxe_member():
    assert room_upgrade("deluxe", True, 1) == "suite"


def test_deluxe_non_member():
    assert room_upgrade("deluxe", False, 1) == "deluxe"


def test_suite_member():
    assert room_upgrade("suite", True, 1) == "suite"


def test_suite_non_member():
    assert room_upgrade("suite", False, 1) == "suite"
