from pydantic import stricturl

from fastapi_auth0_code_flow.schemas.base import BaseModel


class AuthorizationRedirectCookie(BaseModel):
    redirect_uri: stricturl(allowed_schemes={"https"})  # noqa: F821
