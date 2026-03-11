from datetime import datetime


KEYWORDS = [
    "temp", "downloads", "desktop", "documents", "appdata",
    "recent", "startup", "prefetch", "history", "cache",
    "users", "programdata", "windows", "usb"
]


def parse_timestamp(ts):
    if not ts:
        return None
    try:
        return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


def has_keyword(path_text):
    path_lower = path_text.lower()
    return any(keyword in path_lower for keyword in KEYWORDS)


def detect_suspicious_activity(correlated_timeline, recent_days=30):
    suspicious_items = []
    now = datetime.now()

    for event in correlated_timeline:
        item = event.get("item", "")
        created = parse_timestamp(event.get("created", ""))
        modified = parse_timestamp(event.get("modified", ""))
        accessed = parse_timestamp(event.get("accessed", ""))

        reasons = []
        score = 0

        for label, ts in [("created", created), ("modified", modified), ("accessed", accessed)]:
            if ts:
                delta_days = (now - ts).days
                if delta_days <= recent_days:
                    reasons.append(f"Recent {label} activity")
                    score += 2
                    break

        timestamp_count = sum(1 for ts in [created, modified, accessed] if ts is not None)
        if timestamp_count >= 3:
            reasons.append("Multiple timeline indicators present")
            score += 2

        if has_keyword(item):
            reasons.append("Forensically relevant path")
            score += 3

        if created and modified and created != modified:
            reasons.append("Post-creation modification detected")
            score += 2

        if modified and accessed and accessed > modified:
            reasons.append("Access occurred after modification")
            score += 1

        if score > 0:
            suspicious_items.append({
                "item": item,
                "source": event.get("source", ""),
                "created": event.get("created", ""),
                "modified": event.get("modified", ""),
                "accessed": event.get("accessed", ""),
                "event_types": event.get("event_types", ""),
                "event_count": event.get("event_count", 0),
                "confidence": event.get("confidence", ""),
                "suspicion_score": score,
                "reasons": "; ".join(reasons)
            })

    suspicious_items.sort(key=lambda x: x["suspicion_score"], reverse=True)
    return suspicious_items