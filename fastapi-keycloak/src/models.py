from pydantic import BaseModel, Field
from typing import Optional


class TokenRequest(BaseModel):
    username: str = Field(..., example="user123")
    password: str = Field(..., example="pass123")


class TokenResponse(BaseModel):
    access_token: str = Field(..., example="chert o pert")
    token_type: str = Field(default="bearer", const=True)


class UserInfo(BaseModel):
    preferred_username: str
    email: Optional[str] = Field(default=None, example="user@example.com")
    full_name: Optional[str] = Field(default=None, example="vahinuxer")

AuthRequest = TokenRequest
AuthResponse = TokenResponse
UserProfile = UserInfo
