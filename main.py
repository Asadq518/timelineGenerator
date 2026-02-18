from modes.live_mode import collect_live_events
from modes.offline_mode import collect_offline_events
from core.timeline import generate_timeline
import csv, json, os


def save_output(timeline):
    # Ensure output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    csv_path = os.path.join(output_dir, "timeline.csv")
    json_path = os.path.join(output_dir, "timeline.json")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=timeline[0].keys())
        writer.writeheader()
        writer.writerows(timeline)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(timeline, f, indent=4)

    print(f"[+] Timeline saved to {output_dir}/")


def main():
    print("Running from:", os.getcwd())
    print("1. Live System Timeline")
    print("2. Offline Evidence Timeline")

    choice = input("Choose mode: ")

    if choice == "1":
        events = collect_live_events()
    else:
        path = input("Enter file or folder path: ")
        events = collect_offline_events(path)

    timeline = generate_timeline(events)

    if timeline:
        save_output(timeline)
        print("Timeline generated.")

if __name__ == "__main__":
    main()
