from datetime import datetime


def generate_timeline(events):
    """
    Sort events chronologically.
    """
    try:
        return sorted(
            events,
            key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S")
        )
    except Exception as e:
        print(f"Timeline generation error: {e}")
        return []