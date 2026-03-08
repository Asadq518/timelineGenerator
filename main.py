import os
import csv
import json
from datetime import datetime

from modes.live_mode import collect_live_events
from modes.mounted_mode import collect_mounted_events
from core.timeline import generate_timeline
from core.correlator import correlate_events
from visualization.timeline_visualizer import generate_activity_chart, generate_source_chart
from core.suspicious_detector import detect_suspicious_activity
from core.investigation_summary import summarise_timeline

def banner():
    print("""
======================================================================
        Automated Digital Evidence Timeline Generator
======================================================================

████████╗███████╗███████╗███████╗███████╗██╗██████╗ ███████╗
╚══██╔══╝██╔════╝██╔════╝██╔════╝██╔════╝██║██╔══██╗██╔════╝
   ██║   █████╗  █████╗  ███████╗███████╗██║██║  ██║█████╗
   ██║   ██╔══╝  ██╔══╝  ╚════██║╚════██║██║██║  ██║██╔══╝
   ██║   ███████╗███████╗███████║███████║██║██████╔╝███████╗
   ╚═╝   ╚══════╝╚══════╝╚══════╝╚══════╝╚═╝╚═════╝ ╚══════╝

                TEESSIDE UNIVERSITY
       MSc Digital Forensics & Cyber Investigation

Author: Asad Rajput
Supervisor: Harry Stewart

======================================================================
""")

def investigator_info():
    investigator = input("Investigator Name: ")
    case_id = input("Case ID: ")

    print()
    print(f"Investigator: {investigator}")
    print(f"Case ID: {case_id}")
    print(f"Start Time: {datetime.now()}")
    print()

    return investigator, case_id

def create_case_folder(case_id: str) -> str:
    base_dir = "cases"
    case_dir = os.path.join(base_dir, case_id)
    os.makedirs(case_dir, exist_ok=True)
    return case_dir

def save_output(timeline, output_dir):
    if not timeline:
        print("No timeline events found.")
        return

    csv_path = os.path.join(output_dir, "timeline.csv")
    json_path = os.path.join(output_dir, "timeline.json")

    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=timeline[0].keys())
        writer.writeheader()
        writer.writerows(timeline)

    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(timeline, json_file, indent=4)

    print(f"[+] Timeline CSV saved to: {csv_path}")
    print(f"[+] Timeline JSON saved to: {json_path}")

def save_suspicious_output(suspicious_items, output_dir):
    if not suspicious_items:
        print("No suspicious items detected.")
        return

    csv_path = os.path.join(output_dir, "suspicious_activity.csv")
    json_path = os.path.join(output_dir, "suspicious_activity.json")

    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=suspicious_items[0].keys())
        writer.writeheader()
        writer.writerows(suspicious_items)

    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(suspicious_items, json_file, indent=4)

    print(f"[+] Suspicious activity CSV saved to: {csv_path}")
    print(f"[+] Suspicious activity JSON saved to: {json_path}")

def save_summary(summary, output_dir):
    summary_path = os.path.join(output_dir, "investigation_summary.json")

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)

    print(f"[+] Investigation summary saved to: {summary_path}")

def main():
    banner()

    investigator, case_id = investigator_info()
    output_dir = create_case_folder(case_id)

    print("Select Analysis Mode")
    print("1. Live PC Analysis")
    print("2. Mounted Evidence Drive Analysis")
    print("-" * 55)

    choice = input("Select mode (1 or 2): ").strip()

    events = []

    if choice == "1":
        print("[*] Running live system analysis...")
        events = collect_live_events()

    elif choice == "2":
        drive_path = input("Enter mounted drive path (example I:\\): ").strip()

        if not drive_path.endswith("\\"):
            drive_path += "\\"

        print(f"[*] Running mounted evidence analysis on {drive_path} ...")
        events = collect_mounted_events(drive_path)

    else:
        print("Invalid choice.")
        return
    
    print(f"[*] Events collected: {len(events)}")

    timeline = generate_timeline(events)
    print(f"[*] Timeline events sorted: {len(timeline)}")

    correlated_timeline = correlate_events(timeline)
    print(f"[*] Correlated events: {len(correlated_timeline)}")

    save_output(correlated_timeline, output_dir)

    generate_activity_chart(correlated_timeline, output_dir)
    generate_source_chart(correlated_timeline, output_dir)

    suspicious_items = detect_suspicious_activity(correlated_timeline)
    print(f"[*] Suspicious items detected: {len(suspicious_items)}")
    save_suspicious_output(suspicious_items, output_dir)

    summary = summarise_timeline(correlated_timeline)
    save_summary(summary, output_dir)

    print(f"[+] Case results saved in: {output_dir}")
    print("[+] Done.")

if __name__ == "__main__":
    main()