def assign_confidence(event):
    """
    Assign confidence based on event source
    """
    source = event.get("source", "").lower()

    if "file system" in source:
        return "High"
    elif "offline" in source:
        return "Medium"
    else:
        return "Low"
