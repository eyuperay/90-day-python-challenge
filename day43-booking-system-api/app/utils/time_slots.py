from datetime import datetime, timedelta


def generate_slots(
    avail_start: datetime,
    avail_end: datetime,
    duration_minutes: int,
    busy_windows: list[tuple[datetime, datetime]],
) -> list[tuple[datetime, datetime]]:
    """
    Generate non-overlapping time slots within [avail_start, avail_end],
    each of `duration_minutes` length, excluding any window in `busy_windows`.

    Returns a list of (slot_start, slot_end) tuples.

    Example:
        avail_start = 09:00, avail_end = 17:00, duration = 60 min
        busy_windows = [(10:00, 11:00)]
        → [(09:00, 10:00), (11:00, 12:00), (12:00, 13:00), ..., (16:00, 17:00)]
    """
    slots: list[tuple[datetime, datetime]] = []
    duration = timedelta(minutes=duration_minutes)
    cursor = avail_start

    while cursor + duration <= avail_end:
        slot_end = cursor + duration
        # Check if this slot overlaps with any busy window
        overlaps = any(
            cursor < busy_end and slot_end > busy_start
            for busy_start, busy_end in busy_windows
        )
        if not overlaps:
            slots.append((cursor, slot_end))
        cursor += duration  # advance by full slot length regardless

    return slots


def is_within_window(dt: datetime, window_start: datetime, window_end: datetime) -> bool:
    """Return True if dt falls within [window_start, window_end)."""
    return window_start <= dt < window_end


def slots_overlap(
    a_start: datetime, a_end: datetime, b_start: datetime, b_end: datetime
) -> bool:
    """Return True if two time windows overlap (exclusive end)."""
    return a_start < b_end and a_end > b_start
