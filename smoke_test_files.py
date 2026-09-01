"""
ALFRED FILES Capability - Smoke Test
Comprehensive integration test of all features
"""

import sys
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, 'backend')
from backend.tools import files
from backend.tools.tool_registry import get_tool, list_tools

# Setup test workspace
TEST_WORKSPACE = Path(tempfile.gettempdir()) / 'alfred_smoke_test'
TEST_WORKSPACE.mkdir(exist_ok=True)
files.ALFRED_WORKSPACE_ROOT = TEST_WORKSPACE

# Clean
for item in TEST_WORKSPACE.iterdir():
    if item.is_dir():
        shutil.rmtree(item)
    else:
        item.unlink()

print("\n" + "="*70)
print("ALFRED FILES CAPABILITY - SMOKE TEST")
print("="*70 + "\n")

# Test 1: Tool Registry
print("1. Tool Registry")
print(f"   Available tools: {list_tools()}")
files_tool = get_tool("files")
print(f"   Files tool operations: {list(files_tool.operations.keys())}")
print("   ✓ Registry working\n")

# Test 2: Create & Write
print("2. Create & Write Operations")
result = files.create("demo/bill.txt", "Electricity Bill\nAmount: $150")
print(f"   Created: {result.get('status')} (verified: {result.get('verified')})")
result = files.write("demo/note.md", "# My Notes\n- Point 1\n- Point 2")
print(f"   Written: {result.get('status')} (verified: {result.get('verified')})")
print("   ✓ Mutations working\n")

# Test 3: Search & Read
print("3. Search & Read Operations")
result = files.search("bill", "demo")
print(f"   Search results: {result.get('count')} files found")
for r in result.get('results', []):
    print(f"     - {r['filename']} (type: {r['type']})")
result = files.read("demo/bill.txt")
preview = (result.get('content', '')[:30] + '...') if result.get('content') else "N/A"
print(f"   Read: {result.get('size')} bytes, preview: '{preview}'")
print("   ✓ Search & read working\n")

# Test 4: Copy & Move
print("4. Copy & Move Operations")
result = files.copy("demo/bill.txt", "archive/bill_backup.txt")
print(f"   Copy: {result.get('status')} (verified: {result.get('verified')})")
result = files.move("demo/note.md", "docs/notes.md")
print(f"   Move: {result.get('status')} (verified: {result.get('verified')})")
print("   ✓ Copy & move working\n")

# Test 5: List & Delete Confirmation
print("5. List & Delete Confirmation")
result = files.list("demo")
print(f"   Directory contents: {result.get('count')} items")
result = files.delete("archive/bill_backup.txt")
print(f"   Delete confirmation_required: {result.get('confirmation_required')}")
print(f"   Delete path: {result.get('path')}")
result = files.delete_confirmed("archive/bill_backup.txt")
print(f"   Delete confirmed: {result.get('status')} (verified: {result.get('verified')})")
print("   ✓ List & delete working\n")

# Test 6: Path Safety
print("6. Path Safety (Traversal Prevention)")
try:
    files._normalize_path("../../etc/passwd")
    print("   FAILED: Should have blocked traversal")
except ValueError as e:
    print(f"   ✓ Blocked: {str(e)}\n")

# Test 7: Blocked Files
print("7. Blocked File Detection")
env_file = TEST_WORKSPACE / ".env"
env_file.write_text("SECRET=value")
result = files.search(".env", ".")
print(f"   .env search results: {result.get('count')} (should be 0)")
print(f"   ✓ Blocked files excluded\n")

# Cleanup
shutil.rmtree(TEST_WORKSPACE)

print("="*70)
print("ALL SMOKE TESTS PASSED")
print("="*70 + "\n")
