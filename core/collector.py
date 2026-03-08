import os
from datetime import datetime
from utils.confidence import assign_confidence


def safe_format_timestamp(ts_value):
    """
    Convert a timestamp to a standard string format.
    """
    try:
        if ts_value and ts_value > 0:
            return datetime.fromtimestamp(ts_value).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return None
    return None


def collect_filesystem_events(path, source_name="File System", max_files=5000):
    """
    Recursively collect real filesystem timestamp events from a file or directory.

    Args:
        path (str): File or directory path
        source_name (str): Name of the evidence source
        max_files (int): Limit to avoid huge scans

    Returns:
        list: Timeline event dictionaries
    """
    events = []
    file_count = 0

    if not os.path.exists(path):
        print(f"Path not found: {path}")
        return events

    def add_file_events(item_path):
        nonlocal file_count
        if file_count >= max_files:
            return

        try:
            stats = os.stat(item_path)

            timestamps = {
                "Created": stats.st_ctime,
                "Modified": stats.st_mtime,
                "Accessed": stats.st_atime,
            }

            for event_label, raw_ts in timestamps.items():
                formatted_ts = safe_format_timestamp(raw_ts)
                if not formatted_ts:
                    continue

                event = {
                    "timestamp": formatted_ts,
                    "source": source_name,
                    "event_type": f"File {event_label}",
                    "description": f"{event_label}: {item_path}",
                }
                event["confidence"] = assign_confidence(event)
                events.append(event)

            file_count += 1

        except Exception:
            pass

    if os.path.isfile(path):
        add_file_events(path)
        return events

    for root, dirs, files in os.walk(path):
        for name in files:
            if file_count >= max_files:
                break
            full_path = os.path.join(root, name)
            add_file_events(full_path)

        if file_count >= max_files:
            break

    return events