import os
from pathlib import Path
from typing import List, Dict, Any

DEMO_DATA_DIR = Path(__file__).parent.parent.parent / "demo_data"
DOCS_DIR = DEMO_DATA_DIR / "documents"

def search(query: str = "") -> List[Dict[str, str]]:
    if not DOCS_DIR.exists():
        DOCS_DIR.mkdir(parents=True, exist_ok=True)
        
    results = []
    for file in DOCS_DIR.iterdir():
        if file.is_file():
            if query.lower() in file.name.lower():
                results.append({"filename": file.name, "path": str(file)})
    
    # Simple simulated replanning hook: if query doesn't exactly match and they search for exactly "Rahul project report"
    if query == "Rahul project report" and not any(r["filename"] == "Rahul project report" for r in results):
        return []

    return results

def read(filename: str) -> Dict[str, str]:
    file_path = DOCS_DIR / filename
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return {"filename": filename, "content": f.read()}
    return {"error": "File not found"}

def create(filename: str, content: str) -> Dict[str, str]:
    if not DOCS_DIR.exists():
        DOCS_DIR.mkdir(parents=True, exist_ok=True)
        
    file_path = DOCS_DIR / filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    return {"filename": filename, "status": "created"}
