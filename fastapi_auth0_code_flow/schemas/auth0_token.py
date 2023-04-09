from typing import Optional

from fastapi_auth0_code_flow.schemas.base import BaseModel

# from fastapi_auth0_code_flow.schemas.json_web_token import JSONWebToken
# from fastapi_auth0_code_flow.schemas.user import User


class Auth0Token(BaseModel):
    access_token: str
    expires_in: int
    id_token: str
    refresh_token: Optional[str] = None
    scope: str
    token_type: str

    def authorization_header(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    # #TODO def access_token(self) -> JSONWebToken:
    # #TODO     return access_token

    # #TODO # https://auth0.com/docs/secure/tokens/id-tokens/id-token-structure
    # #TODO def id_token(self) -> User:
    # #TODO     return id_token
