import pytest
from agent.tools import send_email, create_document, update_calendar_event, require_approval

def test_require_approval_helper():
    result = require_approval("email", "Send email", "Gmail")
    assert result["success"] is True
    assert result["approval_required"] is True
    assert result["approval"]["type"] == "email"

def test_send_email_requires_approval():
    result = send_email("user123", "test@example.com", "Hello", "World", is_approved=False)
    assert result["success"] is True
    assert result["approval_required"] is True
    assert result["approval"]["type"] == "email"
    assert "Send email" in result["approval"]["title"]

def test_create_document_requires_approval():
    result = create_document("user123", "My Doc", is_approved=False)
    assert result["success"] is True
    assert result["approval_required"] is True
    assert result["approval"]["type"] == "docs"
    assert "Create document" in result["approval"]["title"]

def test_update_calendar_event_requires_approval():
    result = update_calendar_event("user123", "event123", summary="New Title", is_approved=False)
    assert result["success"] is True
    assert result["approval_required"] is True
    assert result["approval"]["type"] == "calendar"
    assert "Update event" in result["approval"]["title"]
