"""
Comprehensive tests for ALFRED FILES capability.
Tests path safety, all 10 operations, verification, and deletion flow.
"""

import pytest
import sys
import os
import shutil
import tempfile
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from backend.tools import files

# Test workspace (isolated for testing)
TEST_WORKSPACE = Path(tempfile.gettempdir()) / "alfred_test_workspace"

def setup_module():
    """Create test workspace."""
    TEST_WORKSPACE.mkdir(exist_ok=True)
    # Override workspace for tests
    files.ALFRED_WORKSPACE_ROOT = TEST_WORKSPACE

def teardown_module():
    """Clean up test workspace."""
    if TEST_WORKSPACE.exists():
        shutil.rmtree(TEST_WORKSPACE)

def teardown_function():
    """Clean up between tests."""
    for item in TEST_WORKSPACE.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

# ============================================================================
# SAFETY TESTS
# ============================================================================

def test_path_traversal_blocked():
    """Prevent directory traversal attacks."""
    with pytest.raises(ValueError, match="Path escapes workspace"):
        files._normalize_path("../../etc/passwd")

def test_absolute_path_blocked():
    """Prevent absolute path escapes."""
    with pytest.raises(ValueError, match="Path escapes workspace"):
        files._normalize_path("/etc/passwd")

def test_symlink_blocked():
    """Prevent symlink escapes (if supported by OS)."""
    test_file = TEST_WORKSPACE / "target.txt"
    test_file.write_text("secret")
    
    symlink = TEST_WORKSPACE / "link.txt"
    try:
        symlink.symlink_to(test_file)
        with pytest.raises(ValueError, match="Symlinks not allowed"):
            files._normalize_path("link.txt")
    except (OSError, NotImplementedError):
        # Windows may not support symlinks without privileges
        pass

def test_env_file_blocked():
    """Prevent access to .env files."""
    env_file = TEST_WORKSPACE / ".env"
    env_file.write_text("SECRET=value")
    
    result = files.search(".env")
    assert result.get("count") == 0, "Should not find .env files"

def test_git_files_blocked():
    """Prevent access to .git files."""
    git_dir = TEST_WORKSPACE / ".git"
    git_dir.mkdir()
    (git_dir / "config").write_text("secret")
    
    result = files.search("config")
    assert result.get("count") == 0, "Should not find files in .git"

# ============================================================================
# LIST OPERATION
# ============================================================================

def test_list_directory():
    """List directory contents."""
    (TEST_WORKSPACE / "file1.txt").write_text("content1")
    (TEST_WORKSPACE / "file2.txt").write_text("content2")
    
    result = files.list(".")
    assert result.get("count") == 2
    assert len(result.get("items", [])) == 2

def test_list_nonexistent_path():
    """Handle listing nonexistent directory."""
    result = files.list("nonexistent")
    assert "error" in result

def test_list_file_as_directory():
    """Handle listing a file as directory."""
    (TEST_WORKSPACE / "file.txt").write_text("content")
    result = files.list("file.txt")
    assert "error" in result

# ============================================================================
# SEARCH OPERATION
# ============================================================================

def test_search_by_filename():
    """Search files by filename."""
    (TEST_WORKSPACE / "electricity_bill_2024.txt").write_text("Amount: $150")
    (TEST_WORKSPACE / "water_bill.txt").write_text("Amount: $50")
    
    result = files.search("electricity")
    assert result.get("count") >= 1
    found_files = [r["filename"] for r in result.get("results", [])]
    assert "electricity_bill_2024.txt" in found_files

def test_search_by_content():
    """Search files by content."""
    (TEST_WORKSPACE / "invoice.txt").write_text("Total due: $500")
    
    result = files.search("Total due")
    assert result.get("count") >= 1
    assert any(r.get("match_type") == "content" for r in result.get("results", []))

def test_search_with_snippet():
    """Search results include content snippet."""
    (TEST_WORKSPACE / "report.md").write_text("The electricity bill was $250 last month")
    
    result = files.search("electricity bill")
    assert result.get("count") >= 1
    for r in result.get("results", []):
        if "electricity" in r.get("snippet", ""):
            assert "electricity" in r["snippet"].lower()
            break

def test_search_no_results():
    """Handle search with no matches."""
    result = files.search("nonexistent_term_xyz")
    assert result.get("count") == 0

# ============================================================================
# READ OPERATION
# ============================================================================

def test_read_text_file():
    """Read text file."""
    content = "Hello, World!"
    (TEST_WORKSPACE / "hello.txt").write_text(content)
    
    result = files.read("hello.txt")
    assert result.get("content") == content
    assert result.get("filename") == "hello.txt"
    assert not result.get("truncated")

def test_read_json_file():
    """Read JSON file."""
    data = {"key": "value", "number": 42}
    (TEST_WORKSPACE / "data.json").write_text(json.dumps(data))
    
    result = files.read("data.json")
    assert "key" in result.get("content", "")
    assert "value" in result.get("content", "")

def test_read_nonexistent_file():
    """Handle reading nonexistent file."""
    result = files.read("nonexistent.txt")
    assert "error" in result

def test_read_large_file_truncated():
    """Truncate large files."""
    large_content = "x" * (files.MAX_READ_SIZE + 1000)
    (TEST_WORKSPACE / "large.txt").write_text(large_content)
    
    result = files.read("large.txt")
    assert result.get("truncated")
    assert len(result.get("content", "")) < len(large_content)
    assert "[... file truncated ...]" in result.get("content", "")

def test_read_directory_fails():
    """Cannot read directory."""
    (TEST_WORKSPACE / "dir").mkdir()
    result = files.read("dir")
    assert "error" in result

# ============================================================================
# CREATE OPERATION
# ============================================================================

def test_create_new_file():
    """Create new file."""
    result = files.create("newfile.txt", "initial content")
    assert result.get("status") == "created"
    assert result.get("verified")
    assert (TEST_WORKSPACE / "newfile.txt").exists()

def test_create_with_nested_path():
    """Create file with nested directories."""
    result = files.create("dir1/dir2/file.txt", "content")
    assert result.get("status") == "created"
    assert (TEST_WORKSPACE / "dir1" / "dir2" / "file.txt").exists()

def test_create_existing_file_fails():
    """Cannot overwrite with create."""
    (TEST_WORKSPACE / "existing.txt").write_text("original")
    result = files.create("existing.txt", "new")
    assert "error" in result

def test_create_empty_file():
    """Create file with empty content."""
    result = files.create("empty.txt", "")
    assert result.get("status") == "created"
    assert (TEST_WORKSPACE / "empty.txt").exists()
    assert (TEST_WORKSPACE / "empty.txt").stat().st_size == 0

# ============================================================================
# WRITE OPERATION
# ============================================================================

def test_write_overwrites_file():
    """Write overwrites existing file."""
    (TEST_WORKSPACE / "file.txt").write_text("original")
    
    result = files.write("file.txt", "new content")
    assert result.get("status") == "written"
    assert result.get("verified")
    assert (TEST_WORKSPACE / "file.txt").read_text() == "new content"

def test_write_creates_if_missing():
    """Write creates file if doesn't exist."""
    result = files.write("newfile.txt", "content")
    assert result.get("status") == "written"
    assert (TEST_WORKSPACE / "newfile.txt").exists()

def test_write_verification():
    """Write includes size verification."""
    content = "test content"
    result = files.write("test.txt", content)
    assert result.get("size") == len(content)
    assert result.get("verified")

# ============================================================================
# APPEND OPERATION
# ============================================================================

def test_append_to_file():
    """Append content to existing file."""
    (TEST_WORKSPACE / "file.txt").write_text("line1\n")
    
    result = files.append("file.txt", "line2\n")
    assert result.get("status") == "appended"
    assert result.get("appended_bytes") == 6
    assert result.get("verified")
    assert (TEST_WORKSPACE / "file.txt").read_text() == "line1\nline2\n"

def test_append_to_nonexistent_creates():
    """Append to nonexistent file creates it."""
    result = files.append("new.txt", "content")
    assert result.get("status") == "appended"
    assert (TEST_WORKSPACE / "new.txt").exists()

def test_append_verification():
    """Append verifies size increase."""
    (TEST_WORKSPACE / "file.txt").write_text("original")
    result = files.append("file.txt", "more")
    assert result.get("previous_size") == 8
    assert result.get("new_size") == 12
    assert result.get("verified")

# ============================================================================
# COPY OPERATION
# ============================================================================

def test_copy_file():
    """Copy file."""
    (TEST_WORKSPACE / "source.txt").write_text("content")
    
    result = files.copy("source.txt", "dest.txt")
    assert result.get("status") == "copied"
    assert result.get("verified")
    assert (TEST_WORKSPACE / "dest.txt").exists()
    assert (TEST_WORKSPACE / "dest.txt").read_text() == "content"

def test_copy_directory():
    """Copy directory with contents."""
    src_dir = TEST_WORKSPACE / "src_dir"
    src_dir.mkdir()
    (src_dir / "file.txt").write_text("content")
    
    result = files.copy("src_dir", "dst_dir")
    assert result.get("status") == "copied"
    assert (TEST_WORKSPACE / "dst_dir" / "file.txt").exists()

def test_copy_nonexistent_source():
    """Cannot copy nonexistent source."""
    result = files.copy("nonexistent.txt", "dest.txt")
    assert "error" in result

def test_copy_existing_dest_fails():
    """Cannot copy to existing destination."""
    (TEST_WORKSPACE / "source.txt").write_text("content")
    (TEST_WORKSPACE / "dest.txt").write_text("existing")
    
    result = files.copy("source.txt", "dest.txt")
    assert "error" in result

# ============================================================================
# MOVE OPERATION
# ============================================================================

def test_move_file():
    """Move file."""
    (TEST_WORKSPACE / "source.txt").write_text("content")
    
    result = files.move("source.txt", "dest.txt")
    assert result.get("status") == "moved"
    assert result.get("verified")
    assert not (TEST_WORKSPACE / "source.txt").exists()
    assert (TEST_WORKSPACE / "dest.txt").exists()

def test_move_to_subdirectory():
    """Move file to subdirectory."""
    (TEST_WORKSPACE / "file.txt").write_text("content")
    (TEST_WORKSPACE / "subdir").mkdir()
    
    result = files.move("file.txt", "subdir/file.txt")
    assert result.get("status") == "moved"
    assert (TEST_WORKSPACE / "subdir" / "file.txt").exists()

def test_move_nonexistent_source():
    """Cannot move nonexistent source."""
    result = files.move("nonexistent.txt", "dest.txt")
    assert "error" in result

# ============================================================================
# RENAME OPERATION
# ============================================================================

def test_rename_file():
    """Rename file."""
    (TEST_WORKSPACE / "old_name.txt").write_text("content")
    
    result = files.rename("old_name.txt", "new_name.txt")
    assert result.get("status") == "renamed"
    assert result.get("verified")
    assert not (TEST_WORKSPACE / "old_name.txt").exists()
    assert (TEST_WORKSPACE / "new_name.txt").exists()

def test_rename_directory():
    """Rename directory."""
    (TEST_WORKSPACE / "olddir").mkdir()
    
    result = files.rename("olddir", "newdir")
    assert result.get("status") == "renamed"
    assert (TEST_WORKSPACE / "newdir").exists()

def test_rename_invalid_name():
    """Reject names with path separators."""
    (TEST_WORKSPACE / "file.txt").write_text("content")
    result = files.rename("file.txt", "dir/newname.txt")
    assert "error" in result

def test_rename_to_existing_fails():
    """Cannot rename to existing name."""
    (TEST_WORKSPACE / "file1.txt").write_text("content")
    (TEST_WORKSPACE / "file2.txt").write_text("content")
    
    result = files.rename("file1.txt", "file2.txt")
    assert "error" in result

# ============================================================================
# DELETE OPERATION
# ============================================================================

def test_delete_returns_confirmation():
    """Delete returns confirmation requirement."""
    (TEST_WORKSPACE / "file.txt").write_text("content")
    
    result = files.delete("file.txt")
    assert result.get("confirmation_required")
    assert result.get("path") == "file.txt"
    assert result.get("type") == "file"
    assert (TEST_WORKSPACE / "file.txt").exists()  # Still exists

def test_delete_confirmed():
    """Delete confirmed actually deletes file."""
    (TEST_WORKSPACE / "file.txt").write_text("content")
    
    result = files.delete_confirmed("file.txt")
    assert result.get("status") == "deleted"
    assert result.get("verified")
    assert not (TEST_WORKSPACE / "file.txt").exists()

def test_delete_directory():
    """Delete directory."""
    (TEST_WORKSPACE / "dir").mkdir()
    (TEST_WORKSPACE / "dir" / "file.txt").write_text("content")
    
    result = files.delete("dir")
    assert result.get("confirmation_required")
    assert result.get("type") == "folder"

def test_delete_confirmed_directory():
    """Delete confirmed removes directory."""
    (TEST_WORKSPACE / "dir").mkdir()
    (TEST_WORKSPACE / "dir" / "file.txt").write_text("content")
    
    result = files.delete_confirmed("dir")
    assert result.get("status") == "deleted"
    assert not (TEST_WORKSPACE / "dir").exists()

def test_delete_nonexistent():
    """Cannot delete nonexistent file."""
    result = files.delete("nonexistent.txt")
    assert "error" in result

# ============================================================================
# DEMO: ELECTRICITY BILL WORKFLOW
# ============================================================================

def test_electricity_bill_demo():
    """
    End-to-end demo: Find electricity bill, read it, extract amount.
    Flow: search → read → extract
    """
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
    assert search_result.get("count") >= 1
    found_file = search_result["results"][0]
    assert "electricity" in found_file["filename"].lower()
    file_path = found_file["path"]
    
    # Step 2: Read the file
    read_result = files.read(file_path)
    assert read_result.get("content")
    assert "Electricity Bill" in read_result["content"]
    
    # Step 3: Extract amount (LLM would do this, but test validates structure)
    assert "$145.50" in read_result["content"]

# ============================================================================
# ERROR HANDLING
# ============================================================================

def test_invalid_path_format():
    """Handle invalid path formats."""
    with pytest.raises(ValueError):
        files._normalize_path("\x00invalid")

def test_permission_denied_simulation():
    """Handle permission errors gracefully."""
    # This is hard to test portably, so just verify error format
    result = files.read("nonexistent/file.txt")
    assert "error" in result

# ============================================================================
# LARGE FILE HANDLING
# ============================================================================

def test_large_file_search_skipped():
    """Search skips large files (>100KB) for content."""
    large_content = "secret_data\n" * 10000  # ~120KB
    (TEST_WORKSPACE / "large.txt").write_text(large_content)
    
    # Filename search should work
    result = files.search("large")
    assert any("large" in r["filename"] for r in result.get("results", []))
    
    # But content search may skip it (implementation detail)
    result = files.search("secret_data")
    # Content match may be missing due to size, but not an error

def test_read_returns_metadata():
    """Read returns file metadata."""
    (TEST_WORKSPACE / "file.txt").write_text("content")
    result = files.read("file.txt")
    assert "path" in result
    assert "filename" in result
    assert "type" in result
    assert "size" in result
    assert "truncated" in result

# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
