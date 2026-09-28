import pytest

from interval import Interval
from main import AvailabilityResult, find_availability
from resource_calendar import ResourceCalendar


def test_find_availability_returns_common_free_windows():
    calendars = {
        "machine": ResourceCalendar(
            working=(Interval(0, 120),),
            busy=(Interval(20, 40), Interval(50, 70)),
        ),
        "sensor": ResourceCalendar(
            working=(Interval(10, 130),),
            busy=(Interval(40, 60), Interval(90, 100)),
        ),
        "operator": ResourceCalendar(
            working=(Interval(0, 120),),
            busy=(Interval(0, 10), Interval(70, 80)),
        ),
    }

    result = find_availability(
        calendars=calendars,
        required_resources=("machine", "sensor", "operator"),
        horizon=Interval(0, 120),
        duration=15,
    )

    assert result == AvailabilityResult(
        free_windows=[
            Interval(10, 20),
            Interval(80, 90),
            Interval(100, 120),
        ],
        earliest_slot=Interval(100, 115),
    )

def test_find_availability_handles_overlapping_and_adjacent_intervals():
    calendars = {
        "machine": ResourceCalendar(
            working=(Interval(0, 100),),
            busy=(
                Interval(20, 40),
                Interval(35, 50),
                Interval(50, 60),
            ),
        ),
    }

    result = find_availability(
        calendars=calendars,
        required_resources=("machine",),
        horizon=Interval(0, 100),
        duration=10,
    )

    assert result == AvailabilityResult(
        free_windows=[
            Interval(0, 20),
            Interval(60, 100),
        ],
        earliest_slot=Interval(0, 10),
    )

def test_find_availability_clips_to_horizon():
    calendars = {
        "machine": ResourceCalendar(
            working=(Interval(-20, 100),),
            busy=(Interval(40, 50),),
        ),
    }

    result = find_availability(
        calendars=calendars,
        required_resources=("machine",),
        horizon=Interval(0, 60),
        duration=10,
    )

    assert result == AvailabilityResult(
        free_windows=[
            Interval(0, 40),
            Interval(50, 60),
        ],
        earliest_slot=Interval(0, 10),
    )

def test_find_availability_supports_negative_times():
    calendars = {
        "machine": ResourceCalendar(
            working=(Interval(-60, 0),),
            busy=(Interval(-40, -20),),
        ),
        "sensor": ResourceCalendar(
            working=(Interval(-60, 0),),
            busy=(),
        ),
        "operator": ResourceCalendar(
            working=(Interval(-60, 0),),
            busy=(),
        ),
    }

    result = find_availability(
        calendars=calendars,
        required_resources=("machine", "sensor", "operator"),
        horizon=Interval(-60, 0),
        duration=20,
    )

    assert result == AvailabilityResult(
        free_windows=[
            Interval(-60, -40),
            Interval(-20, 0),
        ],
        earliest_slot=Interval(-60, -40),
    )

def test_find_availability_exactly_fits_duration():
    calendars = {
        "machine": ResourceCalendar(
            working=(Interval(0, 60),),
            busy=(Interval(0, 30),),
        ),
        "sensor": ResourceCalendar(
            working=(Interval(0, 60),),
            busy=(Interval(0, 30),),
        ),
        "operator": ResourceCalendar(
            working=(Interval(0, 60),),
            busy=(Interval(0, 30),),
        ),
    }

    result = find_availability(
        calendars=calendars,
        required_resources=("machine", "sensor", "operator"),
        horizon=Interval(0, 60),
        duration=30,
    )

    assert result.earliest_slot == Interval(30, 60)


def test_find_availability_returns_none_when_duration_does_not_fit():
    calendars = {
        "machine": ResourceCalendar(
            working=(Interval(0, 20),),
            busy=(Interval(0, 10),),
        ),
        "sensor": ResourceCalendar(
            working=(Interval(0, 20),),
            busy=(Interval(0, 10),),
        ),
        "operator": ResourceCalendar(
            working=(Interval(0, 20),),
            busy=(Interval(0, 10),),
        ),
    }

    result = find_availability(
        calendars=calendars,
        required_resources=("machine", "sensor", "operator"),
        horizon=Interval(0, 20),
        duration=15,
    )

    assert result.free_windows == [Interval(10, 20)]
    assert result.earliest_slot is None


def test_find_availability_raises_for_invalid_horizon():
    calendars = {
        "machine": ResourceCalendar(
            working=(Interval(0, 60),),
            busy=(),
        ),
        "sensor": ResourceCalendar(
            working=(Interval(0, 60),),
            busy=(),
        ),
        "operator": ResourceCalendar(
            working=(Interval(0, 60),),
            busy=(),
        ),
    }

    with pytest.raises(ValueError, match="Horizon start must be lower than horizon end"):
        find_availability(
            calendars=calendars,
            required_resources=("machine", "sensor", "operator"),
            horizon=Interval(60, 0),
            duration=15,
        )

def test_find_availability_with_empty_busy():
    calendars = {
        "machine": ResourceCalendar(
            working=(Interval(0, 60),),
            busy=(),
        ),
    }

    result = find_availability(
        calendars=calendars,
        required_resources=("machine",),
        horizon=Interval(0, 60),
        duration=15,
    )

    assert result == AvailabilityResult(
        free_windows=[Interval(0, 60)],
        earliest_slot=Interval(0, 15),
    )

def test_find_availability_handles_empty_busy_and_working():
    calendars = {
        "machine": ResourceCalendar(
            working=(Interval(0, 60),),
            busy=(),
        ),
        "sensor": ResourceCalendar(
            working=(),
            busy=(),
        ),
    }

    result = find_availability(
        calendars=calendars,
        required_resources=("machine", "sensor"),
        horizon=Interval(0, 60),
        duration=15,
    )

    assert result == AvailabilityResult(
        free_windows=[],
        earliest_slot=None,
    )
