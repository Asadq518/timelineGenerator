from core.collector import collect_filesystem_events


def collect_mounted_events(drive_path):
    """
    Collect events from a mounted forensic image drive.
    Example: I:\\
    """
    return collect_filesystem_events(
        drive_path,
        source_name="Mounted Evidence",
        max_files=5000
    )