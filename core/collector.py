import os
from datetime import datetime
from utils.confidence import assign_confidence

def collect_filesystem_events(path):
    events = []

    if not os.path.exists(path):
        return events

    if os.path.isfile(path):
        paths = [path]
    else:
        paths = [os.path.join(path, f) for f in os.listdir(path)]

    for item in paths:
        try:
            stats = os.stat(item)

            timestamps = {
                "Modified": stats.st_mtime,
                "Accessed": stats.st_atime,
                "Created": stats.st_ctime
            }

            for t_type, t_value in timestamps.items():
                event = {
                    "timestamp": datetime.fromtimestamp(
                        t_value
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                    "source": "File System",
                    "event_type": f"File {t_type}",
                    "description": f"{t_type}: {os.path.basename(item)}"
                }

                event["confidence"] = assign_confidence(event)
                events.append(event)

        except Exception as e:
            print(f"Skipped {item}: {e}")

    return events
