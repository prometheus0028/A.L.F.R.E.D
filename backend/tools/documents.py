from .files import write as write_file
from typing import Dict, Any

def create(title: str, content: str, filename: str) -> Dict[str, Any]:
    full_content = f"# {title}\n\n{content}"
    result = write_file(filename, full_content)
    # Ensure we include the verified flag that the executor expects
    return {
        "status": result.get("status", "success"),
        "file_name": filename,
        "title": title,
        "verified": result.get("verified", False),
        "error": result.get("error")
    }
