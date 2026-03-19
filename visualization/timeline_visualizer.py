import os
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt

def generate_event_type_chart(raw_timeline, output_dir):
    if not raw_timeline:
        return

    event_counter = Counter()

    for event in raw_timeline:
        event_type = event.get("event_type", "Unknown")
        event_counter[event_type] += 1

    if not event_counter:
        return

    labels = list(event_counter.keys())
    values = list(event_counter.values())

    plt.figure(figsize=(8, 6))
    plt.bar(labels, values)
    plt.title("Event Type Distribution")
    plt.xlabel("Event Type")
    plt.ylabel("Count")
    plt.xticks(rotation=20)
    plt.tight_layout()

    output_path = os.path.join(output_dir, "event_type_distribution.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"[+] Event type chart saved to: {output_path}")

def generate_daily_activity_chart(raw_timeline, output_dir):
    if not raw_timeline:
        return

    daily_counter = Counter()

    for event in raw_timeline:
        timestamp = event.get("timestamp", "")
        try:
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            day_label = dt.strftime("%Y-%m-%d")
            daily_counter[day_label] += 1
        except ValueError:
            continue

    if not daily_counter:
        return

    sorted_days = sorted(daily_counter.items(), key=lambda x: x[0])
    dates = [item[0] for item in sorted_days]
    counts = [item[1] for item in sorted_days]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, counts, marker="o")
    plt.title("Daily Timeline Activity")
    plt.xlabel("Date")
    plt.ylabel("Number of Events")
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path = os.path.join(output_dir, "daily_activity_timeline.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"[+] Daily activity timeline chart saved to: {output_path}")

def generate_suspicious_score_chart(suspicious_items, output_dir):
    if not suspicious_items:
        return

    sorted_items = sorted(
        suspicious_items,
        key=lambda x: x.get("suspicion_score", 0),
        reverse=True
    )[:10]

    if not sorted_items:
        return

    labels = [
        (os.path.basename(item.get("item", "Unknown")) or item.get("item", "Unknown"))[:30]
        for item in sorted_items
    ]
    scores = [item.get("suspicion_score", 0) for item in sorted_items]

    plt.figure(figsize=(12, 6))
    plt.bar(labels, scores)
    plt.title("Top Suspicious Items by Score")
    plt.xlabel("Item")
    plt.ylabel("Suspicion Score")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    output_path = os.path.join(output_dir, "suspicious_score_chart.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"[+] Suspicious score chart saved to: {output_path}")