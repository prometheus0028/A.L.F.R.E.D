import json
from pathlib import Path
from typing import Dict, Any, List

DEMO_DATA_DIR = Path(__file__).parent.parent.parent / "demo_data"

def search(query: str = "") -> List[Dict[str, Any]]:
    calendar_file = DEMO_DATA_DIR / "calendar.json"
    if not calendar_file.exists():
        return []
    try:
        with open(calendar_file, "r") as f:
            data = json.load(f)
            events = data if isinstance(data, list) else [data]
            return events
    except Exception:
        return []

def get_event(event_id: str) -> Dict[str, Any]:
    events = search()
    for event in events:
        if event.get("id") == event_id or event.get("title") == event_id:
            return event
    return {}
