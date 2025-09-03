from fastapi import HTTPException, Request, status

# Hardcoded authorization token (in production, this should be in environment variables or a secure store)
AUTHORIZATION_TOKEN = "A6484747478B6F8363FD436C79F89"

class AuthMiddleware:
    def __init__(self):
        self.auth_token = AUTHORIZATION_TOKEN
    
    async def __call__(self, request: Request, call_next):
        # Skip auth for health check endpoints and auth endpoints
        if request.url.path in ["/", "/health", "/health/db", "/docs", "/redoc", "/openapi.json", "/api/v1/auth/verify"]:
            return await call_next(request)
        
        # Get authorization token from header
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header is required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if it's a Bearer token
        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format. Use 'Bearer <token>'",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Extract the token
        token = auth_header.split(" ")[1]
        
        # Validate the token
        if token != self.auth_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Add client info to request state for use in routes if needed
        request.state.authenticated = True
        
        return await call_next(request)

# Simple function to get client info from request state
def get_client_info(request: Request) -> dict:
    """
    Get client information from request state
    """
    return {
        "authenticated": getattr(request.state, "authenticated", False)
    }
