import os
from core.collector import collect_filesystem_events

def collect_live_events():
    """
    Collects live system data from user directories
    """
    user_home = os.path.expanduser("~")
    return collect_filesystem_events(user_home)
