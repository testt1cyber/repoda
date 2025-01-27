from functools import wraps
from fastapi import HTTPException, status
from keycloak.exceptions import KeycloakAuthenticationError
from src.config import keycloak_openid
from src.models import UserInfo

class AuthService:
    @classmethod
    def _handle_keycloak_error(cls, operation):
        @wraps(operation)
        def wrapper(*args, **kwargs):
            try:
                return operation(*args, **kwargs)
            except KeycloakAuthenticationError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication failed"
                )
        return wrapper

    @classmethod
    @_handle_keycloak_error
    def authenticate_user(cls, username: str, password: str) -> str:
        token = keycloak_openid.token(username, password)
        return token["access_token"]
    
    @classmethod
    @_handle_keycloak_error
    def verify_token(cls, token: str) -> UserInfo:
        user_info = keycloak_openid.userinfo(token)
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid token"
            )
        return UserInfo(
            preferred_username=user_info["preferred_username"],
            email=user_info.get("email"),
            full_name=user_info.get("name"),
        )
