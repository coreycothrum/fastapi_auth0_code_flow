from dataclasses import dataclass
from typing import Optional

import aiohttp
from jose import jwt
from pydantic import stricturl

from fastapi_auth0_code_flow.config import settings
from fastapi_auth0_code_flow.schemas.base import BaseModel

# #FIXME - access_token + header + whatever


class JSONWebTokenPayload(BaseModel):
    # https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-token-claims
    iss: Optional[
        stricturl(allowed_schemes={"https"})  # noqa: F821
    ]  # issuer (auth0 tenant)
    aud: Optional[list[stricturl(allowed_schemes={"https"})]]  # audience # noqa: F821

    azp: Optional[str]  # authorized party (client ID)

    exp: Optional[int]  # expires at
    iat: Optional[int]  # issued at
    nbf: Optional[int]  # not before at

    sub: Optional[str]  # subject (user)
    jti: Optional[str]  # jwt unique identifier
    scope: Optional[str]


@dataclass
class JSONWebToken:
    token: str

    def authorization_header(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}

    # https://auth0.com/docs/quickstart/backend/python/01-authorization#create-the-jwt-validation-decorator
    async def validate(self) -> JSONWebTokenPayload:
        unverified_header = jwt.get_unverified_header(self.token)

        jwks = {}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
            ) as response:
                jwks = await response.json()

        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                return jwt.decode(
                    self.token,
                    key,
                    algorithms=["RS256"],
                    audience=settings.AUTH0_AUDIENCE,
                    # stupid trailing '/' took forever to figure out...
                    # used https://jwt.io/ to debug
                    issuer=f"{settings.AUTH0_DOMAIN}/",
                )
