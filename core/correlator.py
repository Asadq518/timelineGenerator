def correlate_events(events):
    """
    Group file events by source + item and merge timestamps into one record.
    Also preserve event types for reporting/export.
    """
    grouped = {}

    for event in events:
        description = event.get("description", "")
        source = event.get("source", "")
        confidence = event.get("confidence", "Low")
        timestamp = event.get("timestamp", "")
        event_type = event.get("event_type", "")

        if ": " in description:
            _, item_name = description.split(": ", 1)
        else:
            item_name = description

        key = (source, item_name)

        if key not in grouped:
            grouped[key] = {
                "source": source,
                "item": item_name,
                "created": "",
                "modified": "",
                "accessed": "",
                "confidence": confidence,
                "event_types": set(),
                "event_count": 0
            }

        grouped[key]["event_count"] += 1

        if event_type:
            grouped[key]["event_types"].add(event_type)

        if "Created" in event_type and not grouped[key]["created"]:
            grouped[key]["created"] = timestamp
        elif "Modified" in event_type and not grouped[key]["modified"]:
            grouped[key]["modified"] = timestamp
        elif "Accessed" in event_type and not grouped[key]["accessed"]:
            grouped[key]["accessed"] = timestamp

    correlated = []

    for _, value in grouped.items():
        correlated.append({
            "source": value["source"],
            "item": value["item"],
            "created": value["created"],
            "modified": value["modified"],
            "accessed": value["accessed"],
            "event_types": ", ".join(sorted(value["event_types"])),
            "event_count": value["event_count"],
            "confidence": value["confidence"]
        })

    return correlated