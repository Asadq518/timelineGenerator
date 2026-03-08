import os
from core.collector import collect_filesystem_events


def collect_live_events():
    """
    Collect events from the current live Windows system.
    """
    user_home = os.path.expanduser("~")
    return collect_filesystem_events(
        user_home,
        source_name="Live System",
        max_files=3000
    )