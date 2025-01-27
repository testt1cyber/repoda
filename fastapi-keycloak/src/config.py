from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field
from keycloak import KeycloakOpenID

@lru_cache(maxsize=1)
def initialize_keycloak_client():
    class KeycloakSettings(BaseSettings):
        server_url: str = Field(..., env="KEYCLOAK_SERVER_URL")
        realm: str = Field(..., env="KEYCLOAK_REALM")
        client_id: str = Field(..., env="KEYCLOAK_CLIENT_ID")
        client_secret: str = Field(..., env="KEYCLOAK_CLIENT_SECRET")

        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"

    settings = KeycloakSettings()
    return KeycloakOpenID(
        server_url=settings.server_url,
        realm_name=settings.realm,
        client_id=settings.client_id,
        client_secret_key=settings.client_secret,
    )

def get_openid_config():
    keycloak_client = initialize_keycloak_client()
    return keycloak_client.well_known()
