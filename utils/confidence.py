def assign_confidence(event):
    """
    Assign a confidence level based on event source.
    """
    source = event.get("source", "").lower()

    if "file system" in source:
        return "High"
    if "mounted evidence" in source:
        return "High"
    if "live system" in source:
        return "Medium"

    return "Low"