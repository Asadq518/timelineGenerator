def filter_events_by_types(events, selected_types):
    """
    Filter raw events by selected event types.
    Example selected_types:
    ['File Created', 'File Modified']
    """
    if not selected_types:
        return events

    selected_types = {t.strip().lower() for t in selected_types}

    filtered = []
    for event in events:
        event_type = event.get("event_type", "").strip().lower()
        if event_type in selected_types:
            filtered.append(event)

    return filtered