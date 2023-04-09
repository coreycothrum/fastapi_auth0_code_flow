# https://auth0.com/docs/get-started/authentication-and-authorization-flow/add-login-auth-code-flow
from typing import Optional
import json
import random
import string

import aiohttp

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from pydantic import stricturl

from fastapi_auth0_code_flow import schemas
from fastapi_auth0_code_flow.config import settings
from fastapi_auth0_code_flow.logger import logger
from fastapi_auth0_code_flow.oauth2 import OAuth2AuthorizationCodeRequestForm

router = APIRouter()


@router.get("/logout", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def auth0_logout(
    request: Request,
    redirect_uri: Optional[stricturl(allowed_schemes={"https"})] = None,  # noqa: F821
) -> RedirectResponse:
    """
    logout of auth0 session

    https://auth0.com/docs/authenticate/login/logout
    """
    request.session.clear()

    url = f"{settings.AUTH0_DOMAIN}/v2/logout?client_id={settings.AUTH0_CLIENT_ID}"

    if redirect_uri:
        url += f"&returnTo={redirect_uri}"

    return RedirectResponse(url)


@router.get("/authorize", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_to_auth0_authorize(
    request: Request,
    redirect_uri: Optional[str] = None,
    scope: Optional[str] = None,
    state: Optional[str] = None,
) -> RedirectResponse:
    """
    redirect to <auth0.com>/authorize endpoint (login); then redirect back to <this_server>/oauth/token

    https://auth0.com/docs/api/authentication#authorize-application
    """
    try:
        url = f"{settings.AUTH0_DOMAIN}/authorize?audience={settings.AUTH0_AUDIENCE}"
        redirect_uri = (
            redirect_uri
            if redirect_uri
            else str(request.url).replace("http:", "https:").split("/authorize")[0]
            + "/oauth/token"
        )
        response_type = "code"
        scope = scope if scope else "openid"
        state = (
            state
            if state
            else "".join(random.choices(string.ascii_letters + string.digits, k=32))
        )
        url += f"&client_id={settings.AUTH0_CLIENT_ID}"
        url += f"&redirect_uri={redirect_uri}"
        url += f"&response_type={response_type}"
        url += f"&scope={scope}"
        url += f"&state={state}"

        logger.info(f"RedirectResponse({url})")

        __cookie_timeout_seconds: int = 60
        response = RedirectResponse(url)
        response.set_cookie(
            state,
            json.dumps(
                schemas.AuthorizationRedirectCookie(redirect_uri=redirect_uri).dict()
            ),
            expires=__cookie_timeout_seconds,
            httponly=True,
            max_age=__cookie_timeout_seconds,
            samesite="strict",
            secure=True,
        )

        return response

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/oauth/token", response_model=schemas.Auth0Token)
async def exchange_auth0_code_for_token_from_form(
    form: OAuth2AuthorizationCodeRequestForm = Depends(
        OAuth2AuthorizationCodeRequestForm.from_form
    ),
) -> schemas.Auth0Token:
    """
    this POST method is needed for swagger-ui to work. Otherwise we'll use the GET

    best to not use this directly

    https://auth0.com/docs/api/authentication#get-token
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{settings.AUTH0_DOMAIN}/oauth/token", data=form.dict()
            ) as response:
                rsp = await response.json()
                return rsp

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.get("/oauth/token", response_model=schemas.Auth0Token)
async def exchange_auth0_code_for_token_from_redirect(
    request: Request, code: str, state: str
) -> schemas.Auth0Token:
    """
    we redirect here from /authorize

    exchange code for jwt using <auth0.com>/oauth/token

    https://auth0.com/docs/api/authentication#get-token
    """
    try:
        try:
            session_data = schemas.AuthorizationRedirectCookie(
                **json.loads(request.cookies.get(state))
            )
            request.session.clear()

            data = OAuth2AuthorizationCodeRequestForm(
                code=code,
                client_secret=f"{settings.AUTH0_CLIENT_SECRET}",
                redirect_uri=session_data.redirect_uri,
            )

        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="expected cookie is malformed or missing",
            )

        return await exchange_auth0_code_for_token_from_form(data)

    except HTTPException as e:
        # already logged above # logger.error(e)
        raise e

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
