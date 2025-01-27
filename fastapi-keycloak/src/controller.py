from functools import wraps
from fastapi import Depends, HTTPException, status, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.models import TokenResponse, UserInfo
from src.service import AuthService

def handle_auth_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e) or "Authentication failed"
            )
    return wrapper

class AuthController:
    bearer_scheme = HTTPBearer()

    @classmethod
    def read_root(cls):
        return {
            "message": (
                "Welcome to the Keycloak"
                "Use the /login endpoint to authenticate and /protected to access the protected resource"
            ),
            "documentation": "/docs",
        }

    @classmethod
    @handle_auth_errors
    def login(cls, username: str = Form(...), password: str = Form(...)) -> TokenResponse:
        access_token = AuthService.authenticate_user(username, password)
        return TokenResponse(access_token=access_token)

    @classmethod
    @handle_auth_errors
    def protected_endpoint(
        cls,
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    ) -> UserInfo:
        token = credentials.credentials
        return AuthService.verify_token(token)
