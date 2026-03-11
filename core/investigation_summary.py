from collections import Counter
from datetime import datetime


def summarise_timeline(correlated_timeline):
    total_items = len(correlated_timeline)
    source_counter = Counter(event.get("source", "Unknown") for event in correlated_timeline)

    all_dates = []
    all_event_types = []

    for event in correlated_timeline:
        event_types = event.get("event_types", "")
        if event_types:
            for e in event_types.split(","):
                all_event_types.append(e.strip())

        for field in ["created", "modified", "accessed"]:
            ts = event.get(field, "")
            if ts:
                try:
                    all_dates.append(datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").date())
                except Exception:
                    continue

    peak_date = None
    peak_count = 0

    if all_dates:
        date_counter = Counter(all_dates)
        peak_date, peak_count = date_counter.most_common(1)[0]

    event_type_breakdown = Counter(all_event_types)

    summary = {
        "total_items": total_items,
        "source_breakdown": dict(source_counter),
        "event_type_breakdown": dict(event_type_breakdown),
        "peak_activity_date": str(peak_date) if peak_date else "",
        "peak_activity_count": peak_count
    }

    return summary