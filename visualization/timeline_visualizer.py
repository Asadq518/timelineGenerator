import os
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt


def extract_date(value):
    """
    Extract date part from timestamp string.
    """
    if not value:
        return None

    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").date()
    except Exception:
        return None


def generate_activity_chart(correlated_timeline, output_dir="output"):
    """
    Create a bar chart showing number of timeline activities per day.
    """
    dates = []

    for event in correlated_timeline:
        for key in ["created", "modified", "accessed"]:
            dt = extract_date(event.get(key, ""))
            if dt:
                dates.append(str(dt))

    if not dates:
        print("No dates available for activity chart.")
        return

    counter = Counter(dates)

    sorted_dates = sorted(counter.keys())
    counts = [counter[d] for d in sorted_dates]

    plt.figure(figsize=(12, 6))
    plt.bar(sorted_dates, counts)
    plt.title("Timeline Activity by Date")
    plt.xlabel("Date")
    plt.ylabel("Number of Events")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    chart_path = os.path.join(output_dir, "activity_chart.png")
    plt.savefig(chart_path)
    plt.close()

    print(f"[+] Activity chart saved to: {chart_path}")


def generate_source_chart(correlated_timeline, output_dir="output"):
    """
    Create a bar chart showing number of events by source.
    """
    sources = [event.get("source", "Unknown") for event in correlated_timeline]

    if not sources:
        print("No sources available for source chart.")
        return

    counter = Counter(sources)

    labels = list(counter.keys())
    counts = list(counter.values())

    plt.figure(figsize=(8, 5))
    plt.bar(labels, counts)
    plt.title("Timeline Events by Source")
    plt.xlabel("Source")
    plt.ylabel("Count")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()

    chart_path = os.path.join(output_dir, "source_chart.png")
    plt.savefig(chart_path)
    plt.close()

    print(f"[+] Source chart saved to: {chart_path}")