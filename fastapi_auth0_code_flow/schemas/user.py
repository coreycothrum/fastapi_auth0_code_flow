from datetime import date, datetime
from typing import Optional

from pydantic import EmailStr, HttpUrl

from fastapi_auth0_code_flow.schemas.base import BaseModel


# https://auth0.com/docs/api/authentication#get-user-info
# https://openid.net/specs/openid-connect-core-1_0.html#StandardClaims
class User(BaseModel):
    sub: str

    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    middle_name: Optional[str]
    nickname: Optional[str]
    preferred_username: Optional[str]

    profile: Optional[HttpUrl]
    picture: Optional[HttpUrl]
    website: Optional[HttpUrl]

    email: Optional[EmailStr]
    email_verified: Optional[bool]

    gender: Optional[str]
    birthdate: Optional[date]
    zoneinfo: Optional[str]  # #TODO better validation - "America/Los_Angeles"
    locale: Optional[str]  # #TODO better validation - "en-US"

    phone_number: Optional[str]  # #TODO better validation - "+1 (111) 222-3434"
    phone_number_verified: Optional[bool]

    address: Optional[dict[str, str]]  # #TODO - can we be more specific?

    updated_at: Optional[datetime]
