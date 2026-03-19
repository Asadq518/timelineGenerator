from datetime import datetime


def parse_user_datetime(value):
    """
    Accept either:
    - YYYY-MM-DD
    - YYYY-MM-DD HH:MM:SS
    """
    value = value.strip()
    if not value:
        return None

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    return None


def parse_event_timestamp(value):
    """
    Parse event timestamp in standard format.
    """
    if not value:
        return None

    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def filter_events_by_datetime(events, start_dt=None, end_dt=None):
    """
    Filter events between start and end datetime.
    If start_dt is None, no lower bound is applied.
    If end_dt is None, no upper bound is applied.
    """
    filtered = []

    for event in events:
        event_ts = parse_event_timestamp(event.get("timestamp", ""))
        if not event_ts:
            continue

        if start_dt and event_ts < start_dt:
            continue

        if end_dt and event_ts > end_dt:
            continue

        filtered.append(event)

    return filtered