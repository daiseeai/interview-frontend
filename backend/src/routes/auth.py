from fastapi import APIRouter, Request, HTTPException, status
from pydantic import BaseModel
from src.middleware.auth import get_client_info, AUTHORIZATION_TOKEN

router = APIRouter()

class AuthRequest(BaseModel):
    token: str

class AuthResponse(BaseModel):
    status: str
    message: str

@router.post("/auth/verify", response_model=AuthResponse)
async def verify_token(auth_request: AuthRequest):
    """
    Verify authorization token
    """
    # Validate token
    if auth_request.token == AUTHORIZATION_TOKEN:
        return AuthResponse(
            status="valid",
            message="Authorization token is valid"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization token"
        )

@router.get("/auth/status")
async def auth_status(request: Request):
    """
    Check authentication status using headers
    """
    client_info = get_client_info(request)
    if client_info["authenticated"]:
        return {
            "status": "authenticated",
            "message": "Client is authenticated"
        }
    else:
        return {
            "status": "unauthenticated",
            "message": "Client is not authenticated"
        }
