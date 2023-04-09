from typing import Optional

from fastapi.security.oauth2 import OAuth2AuthorizationCodeBearer
from fastapi.param_functions import Form
from pydantic import stricturl

from fastapi_auth0_code_flow.config import settings
from fastapi_auth0_code_flow.schemas.base import BaseModel

oauth2_bearer = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{settings.AUTH0_ENDPOINT_PREFIX}/authorize",
    tokenUrl=f"{settings.AUTH0_ENDPOINT_PREFIX}/oauth/token",
    scopes={
        # https://auth0.com/docs/get-started/apis/scopes/openid-connect-scopes
        "openid email profile": "OpenID Connect (OIDC) Standard Claims",
    },
)


# adding scopes will require config in your auth0.com profile/tenant
def update_oauth2_bearer_scopes(scopes: dict):
    oauth2_bearer.model.flows.authorizationCode.scopes.update(scopes)


class OAuth2AuthorizationCodeRequestForm(BaseModel):
    client_id: str = f"{settings.AUTH0_CLIENT_ID}"
    client_secret: str
    code: str
    grant_type: str = "authorization_code"
    redirect_uri: Optional[stricturl(allowed_schemes={"https"})] = None  # noqa: F821

    @classmethod
    def from_form(
        cls,
        client_id: str = Form(),
        client_secret: str = Form(),
        code: str = Form(),
        grant_type: str = Form(
            default="authorization_code", regex="authorization_code"
        ),
        redirect_uri: Optional[str] = Form(default=None),
    ):
        return cls(
            client_id=client_id,
            client_secret=client_secret,
            code=code,
            grant_type=grant_type,
            redirect_uri=redirect_uri,
        )
