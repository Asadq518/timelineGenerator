import os
from tqdm import tqdm

def collect_mounted_events(drive_path):

    events = []
    file_list = []

    print("[*] Scanning mounted drive...")

    for root, dirs, files in os.walk(drive_path):
        for name in files:
            file_list.append(os.path.join(root, name))

    for file_path in tqdm(file_list, desc="Processing Files", unit="file"):
        try:
            stat = os.stat(file_path)

            event = {
                "file_path": file_path,
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "accessed": stat.st_atime,
                "source": "filesystem"
            }

            events.append(event)

        except Exception:
            continue

    print(f"[+] Files processed: {len(events)}")

    return events