import datetime
import base64
from email.message import EmailMessage
from integrations.google.client import (
    get_gmail_service,
    get_calendar_service,
    get_drive_service,
    get_docs_service,
    get_sheets_service,
    get_tasks_service
)
from tools import files

def _clean_snippet(snippet: str) -> str:
    import html
    return html.unescape(snippet).replace("&#39;", "'").replace("&quot;", '"')

def require_approval(type_name: str, title: str, vendor: str):
    return {
        "success": True,
        "approval_required": True,
        "approval": {
            "type": type_name,
            "title": title,
            "vendor": vendor,
            "amount": 0
        }
    }

# --- GMAIL TOOLS ---

def search_gmail(user_id: str, query: str, max_results: int = 5):
    try:
        service = get_gmail_service(user_id)
        results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])
        
        output = []
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['Subject', 'From', 'Date']).execute()
            headers = msg_data.get('payload', {}).get('headers', [])
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown Sender')
            date = next((h['value'] for h in headers if h['name'].lower() == 'date'), 'Unknown Date')
            
            output.append({
                "id": msg['id'],
                "subject": subject,
                "from": sender,
                "date": date,
                "snippet": _clean_snippet(msg_data.get('snippet', ''))
            })
        return {"success": True, "data": output}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_gmail_message(user_id: str, message_id: str):
    try:
        service = get_gmail_service(user_id)
        msg_data = service.users().messages().get(userId='me', id=message_id, format='full').execute()
        return {"success": True, "data": msg_data.get('snippet')}
    except Exception as e:
        return {"success": False, "error": str(e)}

def send_email(user_id: str, to: str, subject: str, body: str, is_approved: bool = False):
    if not is_approved:
        return require_approval("email", f"Send email to {to}", "Gmail")
    try:
        service = get_gmail_service(user_id)
        message = EmailMessage()
        message.set_content(body)
        message['To'] = to
        message['Subject'] = subject
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}
        service.users().messages().send(userId="me", body=create_message).execute()
        return {"success": True, "data": "Email sent"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def mark_email_read(user_id: str, message_id: str, is_approved: bool = False):
    if not is_approved:
        return require_approval("email", f"Mark email {message_id} as read", "Gmail")
    try:
        service = get_gmail_service(user_id)
        service.users().messages().modify(userId='me', id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()
        return {"success": True, "data": "Marked read"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def mark_email_unread(user_id: str, message_id: str, is_approved: bool = False):
    if not is_approved:
        return require_approval("email", f"Mark email {message_id} as unread", "Gmail")
    try:
        service = get_gmail_service(user_id)
        service.users().messages().modify(userId='me', id=message_id, body={'addLabelIds': ['UNREAD']}).execute()
        return {"success": True, "data": "Marked unread"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def archive_email(user_id: str, message_id: str, is_approved: bool = False):
    if not is_approved:
        return require_approval("email", f"Archive email {message_id}", "Gmail")
    try:
        service = get_gmail_service(user_id)
        service.users().messages().modify(userId='me', id=message_id, body={'removeLabelIds': ['INBOX']}).execute()
        return {"success": True, "data": "Archived email"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# --- CALENDAR TOOLS ---

def list_calendar_events(user_id: str, max_results: int = 10, time_min: str = None):
    try:
        service = get_calendar_service(user_id)
        if not time_min:
            time_min = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary', timeMin=time_min,
            maxResults=max_results, singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        output = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            output.append({
                "id": event.get('id'),
                "summary": event.get('summary', 'No Title'),
                "start": start,
                "end": end,
                "link": event.get('htmlLink')
            })
        return {"success": True, "data": output}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_calendar_event(user_id: str, event_id: str):
    try:
        service = get_calendar_service(user_id)
        event = service.events().get(calendarId='primary', eventId=event_id).execute()
        return {"success": True, "data": event}
    except Exception as e:
        return {"success": False, "error": str(e)}

def create_calendar_event(user_id: str, summary: str, start_time: str, end_time: str, description: str = "", is_approved: bool = False):
    if not is_approved:
        return require_approval("calendar", f"Create event: {summary}", "Calendar")
    try:
        service = get_calendar_service(user_id)
        event = {
            'summary': summary,
            'description': description,
            'start': {'dateTime': start_time, 'timeZone': 'UTC'},
            'end': {'dateTime': end_time, 'timeZone': 'UTC'},
        }
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        return {"success": True, "data": {"id": event_result.get('id'), "link": event_result.get('htmlLink')}}
    except Exception as e:
        return {"success": False, "error": str(e)}

def update_calendar_event(user_id: str, event_id: str, summary: str = None, start_time: str = None, end_time: str = None, description: str = None, is_approved: bool = False):
    if not is_approved:
        return require_approval("calendar", f"Update event {event_id}", "Calendar")
    try:
        service = get_calendar_service(user_id)
        event = service.events().get(calendarId='primary', eventId=event_id).execute()
        if summary: event['summary'] = summary
        if description: event['description'] = description
        if start_time: event['start']['dateTime'] = start_time
        if end_time: event['end']['dateTime'] = end_time
        updated = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
        return {"success": True, "data": updated.get('htmlLink')}
    except Exception as e:
        return {"success": False, "error": str(e)}

def delete_calendar_event(user_id: str, event_id: str, is_approved: bool = False):
    if not is_approved:
        return require_approval("calendar", f"Delete event {event_id}", "Calendar")
    try:
        service = get_calendar_service(user_id)
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        return {"success": True, "data": "Deleted"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# --- DRIVE TOOLS ---

def search_drive_files(user_id: str, query: str, max_results: int = 5):
    try:
        service = get_drive_service(user_id)
        q = f"name contains '{query}'" if query else ""
        results = service.files().list(q=q, pageSize=max_results, fields="nextPageToken, files(id, name, mimeType)").execute()
        return {"success": True, "data": results.get('files', [])}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_drive_file(user_id: str, file_id: str, mime_type: str):
    try:
        if 'document' in mime_type:
            docs_service = get_docs_service(user_id)
            doc = docs_service.documents().get(documentId=file_id).execute()
            content = ""
            for element in doc.get('body', {}).get('content', []):
                if 'paragraph' in element:
                    for p_elem in element.get('paragraph', {}).get('elements', []):
                        if 'textRun' in p_elem:
                            content += p_elem.get('textRun', {}).get('content', '')
            return {"success": True, "data": content.strip()[:2000]}
            
        elif 'spreadsheet' in mime_type:
            sheets_service = get_sheets_service(user_id)
            sheet = sheets_service.spreadsheets().get(spreadsheetId=file_id).execute()
            if not sheet.get('sheets'): return {"success": False, "error": "No sheets found"}
            first_sheet_name = sheet['sheets'][0]['properties']['title']
            result = sheets_service.spreadsheets().values().get(spreadsheetId=file_id, range=first_sheet_name).execute()
            values = result.get('values', [])
            content = "\\n".join([",".join([str(cell) for cell in row]) for row in values[:50]])
            return {"success": True, "data": content}
        else:
            return {"success": False, "error": f"Unsupported mimeType for direct reading: {mime_type}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# --- DOCS TOOLS ---

def create_document(user_id: str, title: str, is_approved: bool = False):
    if not is_approved:
        return require_approval("docs", f"Create document: {title}", "Docs")
    try:
        service = get_docs_service(user_id)
        doc = service.documents().create(body={'title': title}).execute()
        return {"success": True, "data": {"id": doc.get('documentId'), "title": doc.get('title')}}
    except Exception as e:
        return {"success": False, "error": str(e)}

def append_to_document(user_id: str, document_id: str, text: str, is_approved: bool = False):
    if not is_approved:
        return require_approval("docs", f"Append text to doc {document_id}", "Docs")
    try:
        service = get_docs_service(user_id)
        requests = [{'insertText': {'location': {'index': 1}, 'text': text + "\\n"}}]
        service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
        return {"success": True, "data": "Appended"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# --- SHEETS TOOLS ---

def write_sheet_values(user_id: str, spreadsheet_id: str, range_name: str, values: list, is_approved: bool = False):
    if not is_approved:
        return require_approval("sheets", f"Write to sheet {spreadsheet_id}", "Sheets")
    try:
        service = get_sheets_service(user_id)
        body = {'values': values}
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption="USER_ENTERED", body=body).execute()
        return {"success": True, "data": "Written"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def create_spreadsheet(user_id: str, title: str, is_approved: bool = False):
    if not is_approved:
        return require_approval("sheets", f"Create sheet: {title}", "Sheets")
    try:
        service = get_sheets_service(user_id)
        sheet = service.spreadsheets().create(body={'properties': {'title': title}}).execute()
        return {"success": True, "data": {"id": sheet.get('spreadsheetId')}}
    except Exception as e:
        return {"success": False, "error": str(e)}


# --- TASKS TOOLS ---

def create_task(user_id: str, title: str, notes: str = "", is_approved: bool = False):
    if not is_approved:
        return require_approval("tasks", f"Create task: {title}", "Tasks")
    try:
        service = get_tasks_service(user_id)
        task = {'title': title, 'notes': notes}
        result = service.tasks().insert(tasklist='@default', body=task).execute()
        return {"success": True, "data": {"id": result.get('id'), "title": result.get('title')}}
    except Exception as e:
        return {"success": False, "error": str(e)}

def complete_task(user_id: str, task_id: str, is_approved: bool = False):
    if not is_approved:
        return require_approval("tasks", f"Complete task {task_id}", "Tasks")
    try:
        service = get_tasks_service(user_id)
        task = service.tasks().get(tasklist='@default', task=task_id).execute()
        task['status'] = 'completed'
        service.tasks().update(tasklist='@default', task=task_id, body=task).execute()
        return {"success": True, "data": "Completed"}
    except Exception as e:
        return {"success": False, "error": str(e)}


TOOL_REGISTRY = {
    "gmail.search": search_gmail,
    "gmail.get_message": get_gmail_message,
    "gmail.send": send_email,
    "gmail.mark_read": mark_email_read,
    "gmail.mark_unread": mark_email_unread,
    "gmail.archive": archive_email,
    
    "calendar.list_events": list_calendar_events,
    "calendar.get_event": get_calendar_event,
    "calendar.create_event": create_calendar_event,
    "calendar.update_event": update_calendar_event,
    "calendar.delete_event": delete_calendar_event,
    
    "drive.search_files": search_drive_files,
    "drive.get_file": get_drive_file,
    
    "docs.create": create_document,
    "docs.append": append_to_document,
    
    "sheets.write": write_sheet_values,
    "sheets.create": create_spreadsheet,
    
    "tasks.create": create_task,
    "tasks.complete": complete_task,
    
    "files.read": lambda user_id, **kwargs: files.read(**kwargs),
    "files.create": lambda user_id, **kwargs: files.create(**kwargs),
    "files.write": lambda user_id, **kwargs: files.write(**kwargs),
    "files.append": lambda user_id, **kwargs: files.append(**kwargs),
    "files.search": lambda user_id, **kwargs: files.search(**kwargs),
    "files.list": lambda user_id, **kwargs: files.list(**kwargs),
    "files.delete": lambda user_id, **kwargs: files.delete(**kwargs)
}
