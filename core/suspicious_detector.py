import os


IGNORE_PATH_KEYWORDS = [
    ".vscode",
    ".virtualbox",
    "node_modules",
    "appdata\\local\\programs",
    "appdata\\roaming\\code",
    "packages",
    "cache",
    "temp",
    "__pycache__",
    "matplotlib",
]

IGNORE_EXTENSIONS = [
    ".log",
    ".tmp",
    ".cache",
]


def is_benign(item_path):
    """
    Return True if the file path appears to belong to a common benign
    development, cache, or application folder/file type.
    """
    if not item_path:
        return False

    lower_path = item_path.lower()

    for keyword in IGNORE_PATH_KEYWORDS:
        if keyword in lower_path:
            return True

    _, ext = os.path.splitext(lower_path)
    if ext in IGNORE_EXTENSIONS:
        return True

    return False


def normalise_event_types(event_types):
    """
    Ensure event_types is always a list.
    Handles:
    - list input
    - comma-separated string input
    - empty input
    """
    if not event_types:
        return []

    if isinstance(event_types, list):
        return event_types

    if isinstance(event_types, str):
        return [e.strip() for e in event_types.split(",") if e.strip()]

    return []


def detect_suspicious_activity(correlated_timeline):
    """
    Identify suspicious items from the correlated timeline.

    Scoring logic is heuristic-based and designed to:
    - reward items with multiple event types
    - reward high event counts
    - reward high confidence
    - reward executable / script / archive style extensions
    - reduce false positives by ignoring common benign paths and extensions
    """
    suspicious_items = []

    for item in correlated_timeline:
        item_path = item.get("item", "")

        if is_benign(item_path):
            continue

        if item_path.lower().endswith("ntuser.ini"):
            continue

        event_types = normalise_event_types(item.get("event_types", []))
        event_count = item.get("event_count", 0)
        confidence = item.get("confidence", 0)

        try:
            confidence = float(confidence)
            
        except (ValueError, TypeError):
            confidence = 0.0

        suspicion_score = 0
        reasons = []

        lower_path = item_path.lower()
        _, ext = os.path.splitext(lower_path)

        # Multiple timestamp activity
        if "File Created" in event_types and "File Modified" in event_types:
            suspicion_score += 2
            reasons.append("File was both created and modified")

        if "File Accessed" in event_types and "File Modified" in event_types:
            suspicion_score += 2
            reasons.append("File was both accessed and modified")

        if len(event_types) >= 3:
            suspicion_score += 2
            reasons.append("File has multiple event types")

        # High activity volume
        if event_count >= 3:
            suspicion_score += 1
            reasons.append("File has repeated timeline activity")

        if event_count >= 5:
            suspicion_score += 2
            reasons.append("File has high event frequency")

        if event_count >= 10:
            suspicion_score += 2
            reasons.append("File has very high event frequency")

        # Confidence weighting
        if confidence >= 0.70:
            suspicion_score += 1
            reasons.append("High confidence timeline item")

        if confidence >= 0.90:
            suspicion_score += 1
            reasons.append("Very high confidence timeline item")

        # File type weighting
        suspicious_extensions = {
            ".exe", ".dll", ".bat", ".cmd", ".ps1", ".vbs", ".js",
            ".jar", ".scr", ".zip", ".rar", ".7z", ".py"
        }

        if ext in suspicious_extensions:
            suspicion_score += 2
            reasons.append(f"Potentially interesting file type: {ext}")

        # User/profile/Desktop/Downloads weighting
        interesting_keywords = [
            "downloads",
            "desktop",
            "documents",
            "users\\",
            "recent",
            "startup",
            "temp",
        ]

        for keyword in interesting_keywords:
            if keyword in lower_path:
                suspicion_score += 1
                reasons.append(f"Located in potentially relevant path: {keyword}")
                break

        # Large registry/user artefact style files
        if "ntuser.dat" in lower_path:
            suspicion_score += 2
            reasons.append("User registry hive detected")

        # Keep only stronger items
        if suspicion_score >= 4:
            suspicious_items.append({
                "item": item.get("item", ""),
                "source": item.get("source", ""),
                "created": item.get("created", ""),
                "modified": item.get("modified", ""),
                "accessed": item.get("accessed", ""),
                "event_types": event_types,
                "event_count": event_count,
                "confidence": confidence,
                "suspicion_score": suspicion_score,
                "reasons": "; ".join(reasons)
            })

    suspicious_items.sort(
        key=lambda x: x.get("suspicion_score", 0),
        reverse=True
    )

    return suspicious_items