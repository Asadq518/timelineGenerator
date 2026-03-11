import os
import csv
import json
from datetime import datetime

from core.event_filter import filter_events_by_types
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

Author: Muhammad Asad 
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

def save_output(raw_timeline, correlated_timeline, output_dir):
    if not raw_timeline and not correlated_timeline:
        print("No timeline events found.")
        return

    raw_csv_path = os.path.join(output_dir, "timeline_raw.csv")
    raw_json_path = os.path.join(output_dir, "timeline_raw.json")

    correlated_csv_path = os.path.join(output_dir, "timeline_correlated.csv")
    correlated_json_path = os.path.join(output_dir, "timeline_correlated.json")

    if raw_timeline:
        raw_fields = ["timestamp", "source", "event_type", "description", "confidence"]

        with open(raw_csv_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=raw_fields)
            writer.writeheader()
            writer.writerows(raw_timeline)

        with open(raw_json_path, "w", encoding="utf-8") as json_file:
            json.dump(raw_timeline, json_file, indent=4)

        print(f"[+] Raw timeline CSV saved to: {raw_csv_path}")
        print(f"[+] Raw timeline JSON saved to: {raw_json_path}")

    if correlated_timeline:
        correlated_fields = [
            "source",
            "item",
            "created",
            "modified",
            "accessed",
            "event_types",
            "event_count",
            "confidence"
        ]

        with open(correlated_csv_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=correlated_fields)
            writer.writeheader()
            writer.writerows(correlated_timeline)

        with open(correlated_json_path, "w", encoding="utf-8") as json_file:
            json.dump(correlated_timeline, json_file, indent=4)

        print(f"[+] Correlated timeline CSV saved to: {correlated_csv_path}")
        print(f"[+] Correlated timeline JSON saved to: {correlated_json_path}")

def save_suspicious_output(suspicious_items, output_dir):
    if not suspicious_items:
        print("No suspicious items detected.")
        return

    csv_path = os.path.join(output_dir, "suspicious_activity.csv")
    json_path = os.path.join(output_dir, "suspicious_activity.json")

    fields = [
        "item",
        "source",
        "created",
        "modified",
        "accessed",
        "event_types",
        "event_count",
        "confidence",
        "suspicion_score",
        "reasons"
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
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

    print("\nFilter by event type before export?")
    print("1. All events")
    print("2. File Created only")
    print("3. File Modified only")
    print("4. File Accessed only")
    print("5. Created + Modified")
    print("6. Created + Modified + Accessed")

    filter_choice = input("Select filter option (1-6): ").strip()

    selected_types = None

    if filter_choice == "2":
        selected_types = ["File Created"]
    elif filter_choice == "3":
        selected_types = ["File Modified"]
    elif filter_choice == "4":
        selected_types = ["File Accessed"]
    elif filter_choice == "5":
        selected_types = ["File Created", "File Modified"]
    elif filter_choice == "6":
        selected_types = ["File Created", "File Modified", "File Accessed"]

    filtered_events = filter_events_by_types(events, selected_types)
    print(f"[*] Events after filtering: {len(filtered_events)}")

    raw_timeline = generate_timeline(filtered_events)
    print(f"[*] Timeline events sorted: {len(raw_timeline)}")

    correlated_timeline = correlate_events(raw_timeline)
    print(f"[*] Correlated events: {len(correlated_timeline)}")

    save_output(raw_timeline, correlated_timeline, output_dir)

    generate_activity_chart(correlated_timeline, output_dir)
    generate_source_chart(correlated_timeline, output_dir)

    suspicious_items = detect_suspicious_activity(correlated_timeline)
    print(f"[*] Suspicious items detected: {len(suspicious_items)}")
    save_suspicious_output(suspicious_items, output_dir)

    summary = summarise_timeline(correlated_timeline)
    save_summary(summary, output_dir)

if __name__ == "__main__":
    main()