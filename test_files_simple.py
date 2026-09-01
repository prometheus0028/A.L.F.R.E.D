"""
Unit tests for ALFRED FILES module - can run without server or pytest.
"""

import sys
import os
import shutil
import tempfile
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from backend.tools import files

# Test workspace (isolated for testing)
TEST_WORKSPACE = Path(tempfile.gettempdir()) / "alfred_test_workspace"

def setup():
    """Create test workspace."""
    TEST_WORKSPACE.mkdir(exist_ok=True)
    # Override workspace for tests
    files.ALFRED_WORKSPACE_ROOT = TEST_WORKSPACE
    print(f"Test workspace: {TEST_WORKSPACE}")

def teardown():
    """Clean up test workspace."""
    if TEST_WORKSPACE.exists():
        shutil.rmtree(TEST_WORKSPACE)

def cleanup_between_tests():
    """Clean up between tests."""
    for item in TEST_WORKSPACE.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

def assert_equal(actual, expected, msg=""):
    if actual != expected:
        raise AssertionError(f"Expected {expected}, got {actual}. {msg}")

def assert_true(value, msg=""):
    if not value:
        raise AssertionError(f"Expected True, got {value}. {msg}")

def assert_false(value, msg=""):
    if value:
        raise AssertionError(f"Expected False, got {value}. {msg}")

def assert_in(item, container, msg=""):
    if item not in container:
        raise AssertionError(f"Expected {item} in {container}. {msg}")

def assert_raises(exc_type, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        raise AssertionError(f"Expected {exc_type} to be raised")
    except exc_type:
        pass

# ============================================================================
# SAFETY TESTS
# ============================================================================

def test_path_traversal_blocked():
    """Prevent directory traversal attacks."""
    print("  Testing path traversal blocking...")
    assert_raises(ValueError, files._normalize_path, "../../etc/passwd")
    print("    ✓ Path traversal blocked")

def test_env_file_blocked():
    """Prevent access to .env files."""
    print("  Testing .env file blocking...")
    env_file = TEST_WORKSPACE / ".env"
    env_file.write_text("SECRET=value")
    
    result = files.search(".env")
    assert_equal(result.get("count"), 0, "Should not find .env files")
    print("    ✓ .env files blocked from search")

# ============================================================================
# LIST OPERATION
# ============================================================================

def test_list_directory():
    """List directory contents."""
    print("  Testing list operation...")
    cleanup_between_tests()
    (TEST_WORKSPACE / "file1.txt").write_text("content1")
    (TEST_WORKSPACE / "file2.txt").write_text("content2")
    
    result = files.list(".")
    assert_equal(result.get("count"), 2, "Should list 2 files")
    assert_equal(len(result.get("items", [])), 2, "Should have 2 items")
    print("    ✓ List directory works")

def test_list_nonexistent_path():
    """Handle listing nonexistent directory."""
    print("  Testing list nonexistent path...")
    cleanup_between_tests()
    result = files.list("nonexistent")
    assert_in("error", result, "Should have error for nonexistent path")
    print("    ✓ Nonexistent path handled")

# ============================================================================
# SEARCH OPERATION
# ============================================================================

def test_search_by_filename():
    """Search files by filename."""
    print("  Testing search by filename...")
    cleanup_between_tests()
    (TEST_WORKSPACE / "electricity_bill_2024.txt").write_text("Amount: $150")
    (TEST_WORKSPACE / "water_bill.txt").write_text("Amount: $50")
    
    result = files.search("electricity")
    assert_true(result.get("count") >= 1, "Should find at least 1 file")
    found_files = [r["filename"] for r in result.get("results", [])]
    assert_in("electricity_bill_2024.txt", found_files, "Should find electricity bill")
    print("    ✓ Search by filename works")

def test_search_by_content():
    """Search files by content."""
    print("  Testing search by content...")
    cleanup_between_tests()
    (TEST_WORKSPACE / "invoice.txt").write_text("Total due: $500")
    
    result = files.search("Total due")
    assert_true(result.get("count") >= 1, "Should find file with matching content")
    print("    ✓ Search by content works")

def test_search_no_results():
    """Handle search with no matches."""
    print("  Testing search with no results...")
    cleanup_between_tests()
    result = files.search("nonexistent_term_xyz_abc")
    assert_equal(result.get("count"), 0, "Should find no results")
    print("    ✓ Empty search handled")

# ============================================================================
# READ OPERATION
# ============================================================================

def test_read_text_file():
    """Read text file."""
    print("  Testing read operation...")
    cleanup_between_tests()
    content = "Hello, World!"
    (TEST_WORKSPACE / "hello.txt").write_text(content)
    
    result = files.read("hello.txt")
    assert_equal(result.get("content"), content, "Content should match")
    assert_equal(result.get("filename"), "hello.txt", "Filename should match")
    assert_false(result.get("truncated"), "Should not be truncated")
    print("    ✓ Read text file works")

def test_read_nonexistent_file():
    """Handle reading nonexistent file."""
    print("  Testing read nonexistent file...")
    cleanup_between_tests()
    result = files.read("nonexistent.txt")
    assert_in("error", result, "Should have error for nonexistent file")
    print("    ✓ Nonexistent file handled")

def test_read_large_file_truncated():
    """Truncate large files."""
    print("  Testing large file truncation...")
    cleanup_between_tests()
    large_content = "x" * (files.MAX_READ_SIZE + 1000)
    (TEST_WORKSPACE / "large.txt").write_text(large_content)
    
    result = files.read("large.txt")
    assert_true(result.get("truncated"), "Should be truncated")
    assert_true(len(result.get("content", "")) < len(large_content), "Content should be smaller")
    assert_in("[... file truncated ...]", result.get("content", ""), "Should indicate truncation")
    print("    ✓ Large file truncation works")

# ============================================================================
# CREATE OPERATION
# ============================================================================

def test_create_new_file():
    """Create new file."""
    print("  Testing create operation...")
    cleanup_between_tests()
    result = files.create("newfile.txt", "initial content")
    assert_equal(result.get("status"), "created", "Status should be 'created'")
    assert_true(result.get("verified"), "Should verify")
    assert_true((TEST_WORKSPACE / "newfile.txt").exists(), "File should exist")
    print("    ✓ Create file works")

def test_create_with_nested_path():
    """Create file with nested directories."""
    print("  Testing create with nested path...")
    cleanup_between_tests()
    result = files.create("dir1/dir2/file.txt", "content")
    assert_equal(result.get("status"), "created", "Status should be 'created'")
    assert_true((TEST_WORKSPACE / "dir1" / "dir2" / "file.txt").exists(), "File should exist")
    print("    ✓ Create with nested path works")

def test_create_existing_file_fails():
    """Cannot overwrite with create."""
    print("  Testing create existing file rejection...")
    cleanup_between_tests()
    (TEST_WORKSPACE / "existing.txt").write_text("original")
    result = files.create("existing.txt", "new")
    assert_in("error", result, "Should have error for existing file")
    print("    ✓ Create on existing file rejected")

# ============================================================================
# WRITE OPERATION
# ============================================================================

def test_write_overwrites_file():
    """Write overwrites existing file."""
    print("  Testing write operation...")
    cleanup_between_tests()
    (TEST_WORKSPACE / "file.txt").write_text("original")
    
    result = files.write("file.txt", "new content")
    assert_equal(result.get("status"), "written", "Status should be 'written'")
    assert_true(result.get("verified"), "Should verify")
    assert_equal((TEST_WORKSPACE / "file.txt").read_text(), "new content", "Content should be updated")
    print("    ✓ Write file works")

def test_write_creates_if_missing():
    """Write creates file if doesn't exist."""
    print("  Testing write create...")
    cleanup_between_tests()
    result = files.write("newfile.txt", "content")
    assert_equal(result.get("status"), "written", "Status should be 'written'")
    assert_true((TEST_WORKSPACE / "newfile.txt").exists(), "File should be created")
    print("    ✓ Write creates missing file")

# ============================================================================
# APPEND OPERATION
# ============================================================================

def test_append_to_file():
    """Append content to existing file."""
    print("  Testing append operation...")
    cleanup_between_tests()
    (TEST_WORKSPACE / "file.txt").write_text("line1\n")
    
    result = files.append("file.txt", "line2\n")
    assert_equal(result.get("status"), "appended", "Status should be 'appended'")
    assert_true(result.get("verified"), "Should verify")
    assert_equal((TEST_WORKSPACE / "file.txt").read_text(), "line1\nline2\n", "Content should be appended")
    print("    ✓ Append file works")

def test_append_to_nonexistent_creates():
    """Append to nonexistent file creates it."""
    print("  Testing append create...")
    cleanup_between_tests()
    result = files.append("new.txt", "content")
    assert_equal(result.get("status"), "appended", "Status should be 'appended'")
    assert_true((TEST_WORKSPACE / "new.txt").exists(), "File should be created")
    print("    ✓ Append creates missing file")

# ============================================================================
# COPY OPERATION
# ============================================================================

def test_copy_file():
    """Copy file."""
    print("  Testing copy operation...")
    cleanup_between_tests()
    (TEST_WORKSPACE / "source.txt").write_text("content")
    
    result = files.copy("source.txt", "dest.txt")
    assert_equal(result.get("status"), "copied", "Status should be 'copied'")
    assert_true(result.get("verified"), "Should verify")
    assert_true((TEST_WORKSPACE / "dest.txt").exists(), "Dest should exist")
    assert_equal((TEST_WORKSPACE / "dest.txt").read_text(), "content", "Content should match")
    print("    ✓ Copy file works")

def test_copy_nonexistent_source():
    """Cannot copy nonexistent source."""
    print("  Testing copy nonexistent...")
    cleanup_between_tests()
    result = files.copy("nonexistent.txt", "dest.txt")
    assert_in("error", result, "Should have error")
    print("    ✓ Copy nonexistent rejected")

# ============================================================================
# MOVE OPERATION
# ============================================================================

def test_move_file():
    """Move file."""
    print("  Testing move operation...")
    cleanup_between_tests()
    (TEST_WORKSPACE / "source.txt").write_text("content")
    
    result = files.move("source.txt", "dest.txt")
    assert_equal(result.get("status"), "moved", "Status should be 'moved'")
    assert_true(result.get("verified"), "Should verify")
    assert_false((TEST_WORKSPACE / "source.txt").exists(), "Source should not exist")
    assert_true((TEST_WORKSPACE / "dest.txt").exists(), "Dest should exist")
    print("    ✓ Move file works")

# ============================================================================
# RENAME OPERATION
# ============================================================================

def test_rename_file():
    """Rename file."""
    print("  Testing rename operation...")
    cleanup_between_tests()
    (TEST_WORKSPACE / "old_name.txt").write_text("content")
    
    result = files.rename("old_name.txt", "new_name.txt")
    assert_equal(result.get("status"), "renamed", "Status should be 'renamed'")
    assert_true(result.get("verified"), "Should verify")
    assert_false((TEST_WORKSPACE / "old_name.txt").exists(), "Old name should not exist")
    assert_true((TEST_WORKSPACE / "new_name.txt").exists(), "New name should exist")
    print("    ✓ Rename file works")

def test_rename_invalid_name():
    """Reject names with path separators."""
    print("  Testing rename invalid name...")
    cleanup_between_tests()
    (TEST_WORKSPACE / "file.txt").write_text("content")
    result = files.rename("file.txt", "dir/newname.txt")
    assert_in("error", result, "Should reject path separators")
    print("    ✓ Invalid rename rejected")

# ============================================================================
# DELETE OPERATION
# ============================================================================

def test_delete_returns_confirmation():
    """Delete returns confirmation requirement."""
    print("  Testing delete confirmation...")
    cleanup_between_tests()
    (TEST_WORKSPACE / "file.txt").write_text("content")
    
    result = files.delete("file.txt")
    assert_true(result.get("confirmation_required"), "Should require confirmation")
    assert_equal(result.get("path"), "file.txt", "Path should be in result")
    assert_true((TEST_WORKSPACE / "file.txt").exists(), "File should still exist")
    print("    ✓ Delete requires confirmation")

def test_delete_confirmed():
    """Delete confirmed actually deletes file."""
    print("  Testing delete confirmed...")
    cleanup_between_tests()
    (TEST_WORKSPACE / "file.txt").write_text("content")
    
    result = files.delete_confirmed("file.txt")
    assert_equal(result.get("status"), "deleted", "Status should be 'deleted'")
    assert_true(result.get("verified"), "Should verify")
    assert_false((TEST_WORKSPACE / "file.txt").exists(), "File should be deleted")
    print("    ✓ Delete confirmed works")

# ============================================================================
# DEMO: ELECTRICITY BILL WORKFLOW
# ============================================================================

def test_electricity_bill_demo():
    """
    End-to-end demo: Find electricity bill, read it, extract amount.
    Flow: search → read → extract
    """
    print("  Testing electricity bill demo workflow...")
    cleanup_between_tests()
    
    # Setup: Create demo files
    (TEST_WORKSPACE / "bills").mkdir()
    (TEST_WORKSPACE / "bills" / "electricity_january_2024.txt").write_text(
        "Electricity Bill - January 2024\n"
        "Billing Period: Jan 1-31, 2024\n"
        "Total Amount Due: $145.50\n"
        "Due Date: Feb 15, 2024"
    )
    (TEST_WORKSPACE / "bills" / "water_january_2024.txt").write_text(
        "Water Bill - January 2024\n"
        "Total Amount: $32.00"
    )
    
    # Step 1: Search for electricity bill
    search_result = files.search("electricity", "bills")
    assert_true(search_result.get("count") >= 1, "Should find electricity bill")
    found_file = search_result["results"][0]
    assert_in("electricity", found_file["filename"].lower(), "Filename should match")
    file_path = found_file["path"]
    
    # Step 2: Read the file
    read_result = files.read(file_path)
    assert_true(read_result.get("content"), "Should have content")
    assert_in("Electricity Bill", read_result["content"], "Should contain bill title")
    
    # Step 3: Extract amount (LLM would do this, but test validates structure)
    assert_in("$145.50", read_result["content"], "Should contain amount")
    print("    ✓ Electricity bill demo works end-to-end")

# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print("ALFRED FILES CAPABILITY - UNIT TESTS")
    print("="*70 + "\n")
    
    tests = [
        # Safety
        ("SAFETY", [
            test_path_traversal_blocked,
            test_env_file_blocked,
        ]),
        # Operations
        ("LIST", [
            test_list_directory,
            test_list_nonexistent_path,
        ]),
        ("SEARCH", [
            test_search_by_filename,
            test_search_by_content,
            test_search_no_results,
        ]),
        ("READ", [
            test_read_text_file,
            test_read_nonexistent_file,
            test_read_large_file_truncated,
        ]),
        ("CREATE", [
            test_create_new_file,
            test_create_with_nested_path,
            test_create_existing_file_fails,
        ]),
        ("WRITE", [
            test_write_overwrites_file,
            test_write_creates_if_missing,
        ]),
        ("APPEND", [
            test_append_to_file,
            test_append_to_nonexistent_creates,
        ]),
        ("COPY", [
            test_copy_file,
            test_copy_nonexistent_source,
        ]),
        ("MOVE", [
            test_move_file,
        ]),
        ("RENAME", [
            test_rename_file,
            test_rename_invalid_name,
        ]),
        ("DELETE", [
            test_delete_returns_confirmation,
            test_delete_confirmed,
        ]),
        ("END-TO-END", [
            test_electricity_bill_demo,
        ]),
    ]
    
    total_passed = 0
    total_failed = 0
    
    for category, category_tests in tests:
        print(f"\n{category}")
        print("-" * 70)
        for test_func in category_tests:
            try:
                test_func()
                total_passed += 1
            except Exception as e:
                print(f"  ✗ {test_func.__name__}")
                print(f"    Error: {e}")
                total_failed += 1
    
    print("\n" + "="*70)
    print(f"RESULTS: {total_passed} passed, {total_failed} failed")
    print("="*70 + "\n")
    
    return total_failed == 0

if __name__ == "__main__":
    setup()
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    finally:
        teardown()
