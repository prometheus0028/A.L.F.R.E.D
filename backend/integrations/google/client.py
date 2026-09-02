import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from storage.credentials import get_google_credentials, save_google_credentials

def get_google_credentials_obj(user_id: str) -> Credentials:
    """
    Constructs a google.oauth2.credentials.Credentials object
    using the stored credentials for the user, refreshing it if expired.
    """
    creds_dict = get_google_credentials(user_id)
    if not creds_dict:
        raise ValueError(f"No Google credentials found for user {user_id}")
    
    creds = Credentials(
        token=creds_dict.get("access_token"),
        refresh_token=creds_dict.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        scopes=creds_dict.get("scope", "").split(" ")
    )
    
    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            # Save the refreshed credentials
            save_google_credentials(user_id, {
                "access_token": creds.token,
                "refresh_token": creds.refresh_token,
                "expires_at": creds.expiry.timestamp() if creds.expiry else None,
                "scope": " ".join(creds.scopes) if creds.scopes else creds_dict.get("scope", "")
            })
        except Exception as e:
            raise ValueError(f"Google reauthorization required for user {user_id}: {str(e)}")
            
    return creds

def get_gmail_service(user_id: str):
    creds = get_google_credentials_obj(user_id)
    return build("gmail", "v1", credentials=creds)

def get_calendar_service(user_id: str):
    creds = get_google_credentials_obj(user_id)
    return build("calendar", "v3", credentials=creds)

def get_drive_service(user_id: str):
    creds = get_google_credentials_obj(user_id)
    return build("drive", "v3", credentials=creds)

def get_docs_service(user_id: str):
    creds = get_google_credentials_obj(user_id)
    return build("docs", "v1", credentials=creds)

def get_sheets_service(user_id: str):
    creds = get_google_credentials_obj(user_id)
    return build("sheets", "v4", credentials=creds)

def get_tasks_service(user_id: str):
    creds = get_google_credentials_obj(user_id)
    return build("tasks", "v1", credentials=creds)
