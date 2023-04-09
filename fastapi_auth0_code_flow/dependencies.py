import aiohttp

from fastapi import Depends, HTTPException, status
from jose import JWTError

from fastapi_auth0_code_flow import schemas
from fastapi_auth0_code_flow.config import settings
from fastapi_auth0_code_flow.logger import logger
from fastapi_auth0_code_flow.oauth2 import oauth2_bearer


async def validate_token(
    jwt: str = Depends(oauth2_bearer),
) -> schemas.JSONWebTokenPayload:
    try:
        jwt_payload = await schemas.JSONWebToken(jwt).validate()
        logger.debug(f"{jwt_payload=}")
        return jwt_payload

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),  # "Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def current_user(
    jwt: str = Depends(oauth2_bearer),
    token: schemas.JSONWebTokenPayload = Depends(validate_token),
) -> schemas.User:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{settings.AUTH0_DOMAIN}/userinfo",
                headers=schemas.JSONWebToken(jwt).authorization_header(),
            ) as response:
                user_info = await response.json()
                logger.debug(f"{user_info=}")
                return user_info

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


class ValidateScopes:
    def __init__(self, required_scopes: list[str]):
        self.required_scopes = required_scopes

    def __call__(self, token: schemas.JSONWebTokenPayload = Depends(validate_token)):
        try:
            granted_scopes = set(token.get("scope", "").split())

            logger.debug(f"{token.sub} {self.required_scopes=} {granted_scopes=}")

            if not set(self.required_scopes).issubset(granted_scopes):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"authorization lacks required scope(s): {self.required_scopes}",
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
