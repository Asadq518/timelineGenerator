from core.collector import collect_filesystem_events

def collect_offline_events(file_path):
    """
    Generates timeline from selected evidence file or directory
    """
    return collect_filesystem_events(file_path)
