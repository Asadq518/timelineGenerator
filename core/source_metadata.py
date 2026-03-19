import os
import shutil
from datetime import datetime


def get_live_source_metadata():
    metadata = {
        "source_mode": "Live PC Analysis",
        "source_path": os.getcwd(),
        "scan_time": str(datetime.now()),
    }

    try:
        usage = shutil.disk_usage(os.path.abspath(os.sep))
        metadata["total_size_bytes"] = usage.total
        metadata["used_size_bytes"] = usage.used
        metadata["free_size_bytes"] = usage.free
    except Exception:
        metadata["total_size_bytes"] = None
        metadata["used_size_bytes"] = None
        metadata["free_size_bytes"] = None

    return metadata


def get_mounted_source_metadata(drive_path):
    metadata = {
        "source_mode": "Mounted Evidence Drive Analysis",
        "source_path": drive_path,
        "scan_time": str(datetime.now()),
        "drive_letter": drive_path,
    }

    try:
        usage = shutil.disk_usage(drive_path)
        metadata["total_size_bytes"] = usage.total
        metadata["used_size_bytes"] = usage.used
        metadata["free_size_bytes"] = usage.free
    except Exception:
        metadata["total_size_bytes"] = None
        metadata["used_size_bytes"] = None
        metadata["free_size_bytes"] = None

    return metadata