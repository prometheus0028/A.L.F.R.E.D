import os
import json
from openai import AsyncOpenAI
from models.task import PlanStep

# Initialize OpenAI Client
# It automatically reads OPENAI_API_KEY from the environment
openai_client = AsyncOpenAI()

# Define the tools JSON Schema for OpenAI Tool Calling or System Prompts
AVAILABLE_TOOLS_SCHEMA = [
    {
        "name": "gmail.search",
        "description": "Searches Gmail for messages matching a query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query (e.g. 'from:boss@company.com')."},
                "max_results": {"type": "integer", "description": "Number of results to return (default 5)."}
            },
            "required": ["query"]
        }
    },
    {
        "name": "gmail.get_message",
        "description": "Get the full text snippet of a specific email message.",
        "parameters": {
            "type": "object",
            "properties": {
                "message_id": {"type": "string", "description": "The ID of the email message."}
            },
            "required": ["message_id"]
        }
    },
    {
        "name": "calendar.list_events",
        "description": "List upcoming calendar events.",
        "parameters": {
            "type": "object",
            "properties": {
                "max_results": {"type": "integer", "description": "Number of events to return."},
                "time_min": {"type": "string", "description": "RFC3339 formatted start time (e.g. 2026-09-02T00:00:00Z). Defaults to now."}
            }
        }
    },
    {
        "name": "calendar.create_event",
        "description": "Create a new calendar event.",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {"type": "string", "description": "Title of the event."},
                "start_time": {"type": "string", "description": "RFC3339 formatted start time (e.g. 2026-09-02T15:00:00Z)."},
                "end_time": {"type": "string", "description": "RFC3339 formatted end time (e.g. 2026-09-02T16:00:00Z)."},
                "description": {"type": "string", "description": "Optional description for the event."}
            },
            "required": ["summary", "start_time", "end_time"]
        }
    },
    {
        "name": "drive.search_files",
        "description": "Search Google Drive for files matching a query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Name or keyword to search for."},
                "max_results": {"type": "integer"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "drive.get_file",
        "description": "Get the plain text content of a Google Doc or Google Sheet.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_id": {"type": "string", "description": "The Google Drive file ID."},
                "mime_type": {"type": "string", "description": "The mimeType of the file (e.g. application/vnd.google-apps.document)."}
            },
            "required": ["file_id", "mime_type"]
        }
    },
    {
        "name": "tasks.create",
        "description": "Create a new task in Google Tasks.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Title of the task."},
                "notes": {"type": "string", "description": "Notes or description for the task."}
            },
            "required": ["title"]
        }
    },
    {
        "name": "gmail.send",
        "description": "Send an email. Requires user approval.",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "Recipient email address."},
                "subject": {"type": "string", "description": "Email subject."},
                "body": {"type": "string", "description": "Email body content."}
            },
            "required": ["to", "subject", "body"]
        }
    },
    {
        "name": "gmail.mark_read",
        "description": "Mark an email as read.",
        "parameters": {
            "type": "object",
            "properties": {
                "message_id": {"type": "string", "description": "The ID of the email message."}
            },
            "required": ["message_id"]
        }
    },
    {
        "name": "gmail.mark_unread",
        "description": "Mark an email as unread.",
        "parameters": {
            "type": "object",
            "properties": {
                "message_id": {"type": "string", "description": "The ID of the email message."}
            },
            "required": ["message_id"]
        }
    },
    {
        "name": "gmail.archive",
        "description": "Archive an email.",
        "parameters": {
            "type": "object",
            "properties": {
                "message_id": {"type": "string", "description": "The ID of the email message."}
            },
            "required": ["message_id"]
        }
    },
    {
        "name": "calendar.get_event",
        "description": "Get details of a specific calendar event.",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {"type": "string", "description": "The ID of the calendar event."}
            },
            "required": ["event_id"]
        }
    },
    {
        "name": "calendar.update_event",
        "description": "Update an existing calendar event. Requires user approval.",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {"type": "string", "description": "The ID of the calendar event."},
                "summary": {"type": "string"},
                "start_time": {"type": "string", "description": "RFC3339 formatted start time."},
                "end_time": {"type": "string", "description": "RFC3339 formatted end time."},
                "description": {"type": "string"}
            },
            "required": ["event_id"]
        }
    },
    {
        "name": "calendar.delete_event",
        "description": "Delete a calendar event. Requires user approval.",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {"type": "string", "description": "The ID of the calendar event."}
            },
            "required": ["event_id"]
        }
    },
    {
        "name": "docs.create",
        "description": "Create a new Google Document. Requires user approval.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Title of the document."}
            },
            "required": ["title"]
        }
    },
    {
        "name": "docs.append",
        "description": "Append text to a Google Document. Requires user approval.",
        "parameters": {
            "type": "object",
            "properties": {
                "document_id": {"type": "string", "description": "ID of the document."},
                "text": {"type": "string", "description": "Text to append."}
            },
            "required": ["document_id", "text"]
        }
    },
    {
        "name": "sheets.create",
        "description": "Create a new Google Spreadsheet. Requires user approval.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Title of the spreadsheet."}
            },
            "required": ["title"]
        }
    },
    {
        "name": "sheets.write",
        "description": "Write values to a Google Spreadsheet range. Requires user approval.",
        "parameters": {
            "type": "object",
            "properties": {
                "spreadsheet_id": {"type": "string", "description": "ID of the spreadsheet."},
                "range_name": {"type": "string", "description": "Range to write to (e.g. 'Sheet1!A1:B2')."},
                "values": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "description": "2D array of values to write."
                }
            },
            "required": ["spreadsheet_id", "range_name", "values"]
        }
    },
    {
        "name": "tasks.complete",
        "description": "Mark a Google Task as completed. Requires user approval.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "The ID of the task."}
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "files.read",
        "description": "Read contents of a file in the workspace.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the file."}
            },
            "required": ["path"]
        }
    },
    {
        "name": "files.write",
        "description": "Overwrite a file with new content. Use this to edit or update files.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the file."},
                "content": {"type": "string", "description": "The new file content."}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "files.create",
        "description": "Create a new file with content.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the file."},
                "content": {"type": "string", "description": "The initial file content."}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "files.delete",
        "description": "Delete a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the file."}
            },
            "required": ["path"]
        }
    },
    {
        "name": "files.list",
        "description": "List files in a directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to directory (default '.')"}
            }
        }
    },
    {
        "name": "files.search",
        "description": "Search for files by name or content.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query."},
                "path": {"type": "string", "description": "Directory to search in."}
            },
            "required": ["query"]
        }
    }
]

async def generate_plan_from_goal(goal: str) -> list[PlanStep]:
    """
    Uses gpt-4o-mini to convert a natural language goal into a structured list of plan steps.
    """
    system_prompt = f"""
    You are ALFRED, an advanced AI agent managing a user's Google Workspace.
    Your task is to take the user's GOAL and break it down into a sequence of executable tool steps.
    
    AVAILABLE TOOLS:
    {json.dumps(AVAILABLE_TOOLS_SCHEMA, indent=2)}
    
    You must output your plan strictly as a JSON array of objects. 
    Each object MUST have the following structure:
    {{
        "id": "step_1",
        "description": "Human readable description of what this step does",
        "tool": "name.of.the.tool",
        "tool_arguments": {{"arg1": "value"}},
        "success_criteria": ["data_found"]
    }}
    
    IMPORTANT: You must ONLY output the raw JSON array. Do not include markdown code blocks (e.g. ```json).
    """
    
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is missing. Using a fallback static plan.")
        return [PlanStep(
            id="step_1",
            description="Fallback: OPENAI_API_KEY is not configured.",
            tool="unknown",
            tool_arguments={},
            success_criteria=["configured_api_key"]
        )]

    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"GOAL: {goal}"}
            ],
            temperature=0.0
        )
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return [PlanStep(
            id="step_1",
            description=f"Fallback: OpenAI Error - {str(e)}",
            tool="unknown",
            tool_arguments={},
            success_criteria=["fix_error"]
        )]
    
    content = response.choices[0].message.content.strip()
    
    # Strip markdown if the model hallucinated it
    if content.startswith("```json"):
        content = content[7:]
    if content.endswith("```"):
        content = content[:-3]
        
    try:
        raw_steps = json.loads(content)
        steps = []
        for raw in raw_steps:
            # We add tool_arguments to PlanStep dynamically by injecting it into the description or storing it.
            # But wait, our current PlanStep model doesn't have tool_arguments.
            # Let's attach them to a new field or serialize them into the description.
            # We'll need to update the PlanStep model in models/task.py to accept kwargs.
            step = PlanStep(
                id=raw["id"],
                description=raw["description"],
                tool=raw["tool"],
                tool_arguments=raw.get("tool_arguments", {}),
                success_criteria=raw.get("success_criteria", []),
            )
            steps.append(step)
        return steps
    except Exception as e:
        print(f"Error parsing LLM plan: {e}")
        print(f"Raw output: {content}")
        # Fallback
        return [PlanStep(id="step_1", description=f"Fallback: {str(e)}", tool="unknown")]
