import json
from pathlib import Path
from typing import Dict, Any, List

DEMO_DATA_DIR = Path(__file__).parent.parent.parent / "demo_data"

def search(query: str = "") -> List[Dict[str, Any]]:
    emails_file = DEMO_DATA_DIR / "emails.json"
    if not emails_file.exists():
        return []
    try:
        with open(emails_file, "r") as f:
            data = json.load(f)
            emails = data if isinstance(data, list) else [data]
            if not query:
                return emails
            
            result = []
            for email in emails:
                if query.lower() in email.get("subject", "").lower() or query.lower() in email.get("body", "").lower():
                    result.append(email)
            return result
    except Exception:
        return []

def read(email_id: str) -> Dict[str, Any]:
    emails = search()
    for email in emails:
        if email.get("id") == email_id:
            return email
    return {}
