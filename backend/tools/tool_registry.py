"""
ALFRED Tool Registry - Central registry for all available tools and operations.

Tools can be dynamically selected by the planner and executor without hardcoding.
Each tool has a module name, operations, and brief descriptions for LLM reasoning.
"""

from typing import Dict, Any, List, Optional, Callable

class ToolOperation:
    """Describes a single tool operation."""
    def __init__(
        self,
        name: str,
        module: str,
        description: str,
        params: Dict[str, str],
        returns: str,
    ):
        self.name = name  # e.g., "search"
        self.module = module  # e.g., "files"
        self.description = description
        self.params = params  # {"param_name": "description"}
        self.returns = returns  # "Returns: ..."

class Tool:
    """Describes a tool with its operations."""
    def __init__(self, name: str, description: str, operations: List[ToolOperation]):
        self.name = name
        self.description = description
        self.operations = {op.name: op for op in operations}

# Define all tools
TOOLS: Dict[str, Tool] = {
    "files": Tool(
        name="files",
        description="File operations (search, read, create, write, move, delete, etc.)",
        operations=[
            ToolOperation(
                name="list",
                module="files",
                description="List files/folders in directory",
                params={"path": "Directory path (relative to workspace)"},
                returns="count, items with name/type/size/modified",
            ),
            ToolOperation(
                name="search",
                module="files",
                description="Search files by name and content. Returns paths, types, sizes, snippets.",
                params={
                    "query": "Search term (filename or content)",
                    "path": "Search root (optional, default='.')",
                    "file_type": "Filter by type (optional, e.g. 'pdf', 'txt')",
                },
                returns="results with path, filename, type, size, modified, snippet",
            ),
            ToolOperation(
                name="read",
                module="files",
                description="Read file content. Large files truncated automatically.",
                params={"path": "File path"},
                returns="filename, type, size, content (truncated if large), truncated flag",
            ),
            ToolOperation(
                name="create",
                module="files",
                description="Create new file with content. Fails if exists.",
                params={
                    "path": "File path",
                    "content": "Initial content (optional, default='')",
                },
                returns="status, path, size, verified",
            ),
            ToolOperation(
                name="write",
                module="files",
                description="Overwrite file content. Creates if doesn't exist.",
                params={
                    "path": "File path",
                    "content": "New content",
                },
                returns="status, path, size, verified",
            ),
            ToolOperation(
                name="append",
                module="files",
                description="Append content to file. Creates if doesn't exist.",
                params={
                    "path": "File path",
                    "content": "Content to append",
                },
                returns="status, path, appended_bytes, new_size, verified",
            ),
            ToolOperation(
                name="copy",
                module="files",
                description="Copy file or directory.",
                params={
                    "source": "Source path",
                    "destination": "Destination path (must not exist)",
                },
                returns="status, source, destination, verified",
            ),
            ToolOperation(
                name="move",
                module="files",
                description="Move file or directory.",
                params={
                    "source": "Source path",
                    "destination": "Destination path (must not exist)",
                },
                returns="status, source, destination, verified",
            ),
            ToolOperation(
                name="rename",
                module="files",
                description="Rename file or folder.",
                params={
                    "path": "File/folder path",
                    "new_name": "New name (no path separators)",
                },
                returns="status, old_path, new_path, verified",
            ),
            ToolOperation(
                name="delete",
                module="files",
                description="Request file/folder deletion. Requires user confirmation.",
                params={"path": "File/folder path"},
                returns="confirmation_required, path, type, size, message",
            ),
        ],
    ),
    "calendar": Tool(
        name="calendar",
        description="Calendar events (search, get event details)",
        operations=[
            ToolOperation(
                name="search",
                module="calendar",
                description="Find calendar events.",
                params={"query": "Search term (optional)"},
                returns="List of events with id, title, date, attendees",
            ),
        ],
    ),
    "email": Tool(
        name="email",
        description="Email operations (search, read)",
        operations=[
            ToolOperation(
                name="search",
                module="email",
                description="Search emails by subject/body.",
                params={"query": "Search term (optional)"},
                returns="List of emails with id, subject, from, body",
            ),
            ToolOperation(
                name="read",
                module="email",
                description="Read full email content.",
                params={"email_id": "Email ID"},
                returns="Email object with full details",
            ),
        ],
    ),
    "documents": Tool(
        name="documents",
        description="Document creation (briefings, summaries)",
        operations=[
            ToolOperation(
                name="create",
                module="documents",
                description="Create a new document (briefing, summary, etc.)",
                params={
                    "title": "Document title",
                    "content": "Document content",
                    "filename": "Output filename",
                },
                returns="status, file_name",
            ),
        ],
    ),
    "finance": Tool(
        name="finance",
        description="Finance operations (invoices, payments)",
        operations=[
            ToolOperation(
                name="list_pending_invoices",
                module="finance",
                description="List all pending invoices.",
                params={},
                returns="List of invoices with id, vendor, amount, currency",
            ),
            ToolOperation(
                name="propose_payment",
                module="finance",
                description="Propose payment for an invoice. May require approval.",
                params={"invoice_id": "Invoice ID"},
                returns="invoice details and policy check result",
            ),
        ],
    ),
}

def get_tool(tool_name: str) -> Optional[Tool]:
    """Get tool by name."""
    return TOOLS.get(tool_name)

def get_operation(tool_name: str, operation: str) -> Optional[ToolOperation]:
    """Get specific operation from a tool."""
    tool = TOOLS.get(tool_name)
    if tool:
        return tool.operations.get(operation)
    return None

def list_tools() -> List[str]:
    """List all available tool names."""
    return list(TOOLS.keys())

def list_operations(tool_name: str) -> List[str]:
    """List all operations for a tool."""
    tool = TOOLS.get(tool_name)
    if tool:
        return list(tool.operations.keys())
    return []

def get_tool_description_for_planner(tool_name: str) -> str:
    """Get compact tool description for planner/LLM."""
    tool = TOOLS.get(tool_name)
    if not tool:
        return ""
    
    ops = ", ".join(tool.operations.keys())
    return f"{tool.name}: {tool.description} (ops: {ops})"

def get_operation_signature(tool_name: str, operation_name: str) -> Dict[str, Any]:
    """Get operation signature for tool dispatch."""
    op = get_operation(tool_name, operation_name)
    if not op:
        return {}
    
    return {
        "tool": tool_name,
        "operation": operation_name,
        "module": op.module,
        "description": op.description,
        "params": op.params,
        "returns": op.returns,
    }
