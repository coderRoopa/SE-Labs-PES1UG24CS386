
import pytest

from hotel_booking import (
    booking_cost,
    cancellation_refund,
    room_upgrade
)


# BOOKING COST TESTS

def test_standard_two_nights():
    assert booking_cost("standard", 2, 2, False) == 4000


def test_deluxe_room():
    assert booking_cost("deluxe", 2, 2, False) == 7000


def test_suite_room():
    assert booking_cost("suite", 1, 2, False) == 6000


def test_unknown_room():
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("invalid", 2, 2, False)


def test_invalid_nights():
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", 0, 2, False)


def test_peak_season():
    assert booking_cost("standard", 2, 2, True) == 5000


def test_extra_guests():
    assert booking_cost("standard", 2, 4, False) == 6000


def test_weekly_discount():
    assert booking_cost("standard", 7, 2, False) == 12600


def test_peak_extra_guests_weekly():
    assert booking_cost("deluxe", 7, 4, True) == 33863


# CANCELLATION REFUND TESTS

def test_full_refund():
    assert cancellation_refund(1000, 10, False) == 1000


def test_half_refund():
    assert cancellation_refund(1000, 3, False) == 500


def test_no_refund():
    assert cancellation_refund(1000, 1, False) == 0


def test_member_refund():
    assert cancellation_refund(1000, 3, True) == 750


def test_member_no_refund_period():
    assert cancellation_refund(1000, 1, True) == 250


# ROOM UPGRADE TESTS

def test_no_free_rooms():
    assert room_upgrade("standard", True, 0) == "standard"


def test_standard_member_upgrade():
    assert room_upgrade("standard", True, 1) == "deluxe"


def test_deluxe_member_upgrade():
    assert room_upgrade("deluxe", True, 1) == "suite"


def test_non_member_no_upgrade():
    assert room_upgrade("standard", False, 1) == "standard"


def test_suite_no_upgrade():
    assert room_upgrade("suite", True, 1) == "suite"
