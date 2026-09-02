import os

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from storage.credentials import save_google_credentials, get_google_credentials, delete_google_credentials

router = APIRouter(prefix="/auth/google", tags=["Google OAuth"])

oauth = OAuth()

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": " ".join([
            "openid",
            "email",
            "profile",
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/gmail.modify",
            "https://www.googleapis.com/auth/calendar.events",
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/documents.readonly",
            "https://www.googleapis.com/auth/documents",
            "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/tasks"
        ])
    },
)

@router.get("/login")
async def google_login(request: Request):
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        access_type="offline",
        prompt="consent",
    )

@router.get("/status")
async def google_status(request: Request):

    user = request.session.get("google_user")

    if not user:
        return {
            "connected": False
        }
        
    creds = get_google_credentials(user["sub"])
    services = {
        "gmail": False,
        "calendar": False,
        "drive": False,
        "docs": False,
        "sheets": False,
        "tasks": False
    }

    if creds and "scope" in creds:
        scopes = creds["scope"]
        services["gmail"] = all(s in scopes for s in ["gmail.readonly", "gmail.send", "gmail.modify"])
        services["calendar"] = "calendar.events" in scopes
        services["drive"] = all(s in scopes for s in ["drive.readonly", "drive.file"])
        services["docs"] = all(s in scopes for s in ["documents.readonly", "documents"])
        services["sheets"] = all(s in scopes for s in ["spreadsheets.readonly", "spreadsheets"])
        services["tasks"] = "tasks" in scopes

    return {
        "connected": True,
        "user": user,
        "services": services
    }
    
@router.get("/callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)

    user_info = token.get("userinfo")

    if not user_info:
        user_info = await oauth.google.parse_id_token(
            request,
            token,
        )

    user_sub = user_info["sub"]
    
    request.session["google_user"] = {
        "sub": user_sub,
        "email": user_info.get("email"),
        "name": user_info.get("name"),
        "picture": user_info.get("picture"),
    }
    
    # Securely store credentials backend-side
    save_google_credentials(user_sub, {
        "access_token": token.get("access_token"),
        "refresh_token": token.get("refresh_token"),
        "expires_at": token.get("expires_at"),
        "scope": token.get("scope", "")
    })

    return RedirectResponse(
        url="http://localhost:5173/dashboard?google=connected"
    )

@router.post("/disconnect")
async def google_disconnect(request: Request):
    user = request.session.get("google_user")
    if user:
        delete_google_credentials(user["sub"])
    request.session.clear()
    return {"connected": False}