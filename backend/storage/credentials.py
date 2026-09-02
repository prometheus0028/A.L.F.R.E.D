from typing import Dict, Optional, Any

# In-memory dictionary for storing user Google credentials
# Key: user_id (Google 'sub' subject ID)
# Value: Dictionary containing access_token, refresh_token, scopes, expires_at
_user_credentials: Dict[str, Dict[str, Any]] = {}

def save_google_credentials(user_id: str, credentials_data: Dict[str, Any]) -> None:
    """
    Save or update Google OAuth credentials for a specific user.
    """
    _user_credentials[user_id] = credentials_data

def get_google_credentials(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve stored Google OAuth credentials for a user.
    """
    return _user_credentials.get(user_id)

def delete_google_credentials(user_id: str) -> None:
    """
    Remove stored Google OAuth credentials for a user (e.g., on disconnect).
    """
    if user_id in _user_credentials:
        del _user_credentials[user_id]
