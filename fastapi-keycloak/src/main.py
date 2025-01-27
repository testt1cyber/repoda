from fastapi import FastAPI, Depends, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.models import TokenResponse, UserInfo
from src.controller import AuthController
from typing import Dict, Any

class AuthAPI:
    def __init__(self):
        self.app = FastAPI()
        self.bearer_scheme = HTTPBearer()
        self.auth_controller = AuthController()
        self._init_routes()
    
    def _init_routes(self) -> None:
        self.app.get("/")(self.read_root)
        self.app.post("/login", response_model=TokenResponse)(self.login)
        self.app.get("/protected", response_model=UserInfo)(self.protected_endpoint)
    
    async def read_root(self) -> Dict[str, str]:
        return self.auth_controller.read_root()
    
    async def login(
        self, 
        username: str = Form(...), 
        password: str = Form(...)
    ) -> TokenResponse:
        return self.auth_controller.login(username, password)
    
    async def protected_endpoint(
        self, 
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> UserInfo:
        return self.auth_controller.protected_endpoint(credentials)

auth_api = AuthAPI()
app = auth_api.app
