def assign_confidence(event):
    source = event.get("source", "").lower()

    base = 0.5

    if "mounted evidence" in source:
        base += 0.3
    elif "file system" in source:
        base += 0.3
    elif "live system" in source:
        base += 0.2

    return min(base, 1.0)