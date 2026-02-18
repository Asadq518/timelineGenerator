from datetime import datetime

def generate_timeline(events):
    return sorted(
        events,
        key=lambda x: datetime.strptime(
            x["timestamp"], "%Y-%m-%d %H:%M:%S"
        )
    )
