from .files import create as create_file
from typing import Dict, Any

def create(title: str, content: str, filename: str) -> Dict[str, Any]:
    full_content = f"# {title}\n\n{content}"
    result = create_file(filename, full_content)
    return {
        "status": "success",
        "file_name": filename,
        "title": title
    }
