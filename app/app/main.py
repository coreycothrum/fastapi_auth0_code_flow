import os

from fastapi import Depends, FastAPI
from fastapi.middleware import Middleware

from starlette.middleware.sessions import SessionMiddleware

from fastapi_auth0_code_flow.api.router import api_router as auth0_api_router
from fastapi_auth0_code_flow.config import settings as auth0_settings
from fastapi_auth0_code_flow.dependencies import (
    current_user,
    ValidateScopes,
    validate_token,
)
from fastapi_auth0_code_flow.oauth2 import update_oauth2_bearer_scopes
from fastapi_auth0_code_flow.schemas import JSONWebTokenPayload, User

from app.core.config import settings

################################################################################
# extend fastapi_auth0_code_flow with our application specific scope(s)
# these will require config in your auth0.com profile/tenant
app_scopes = {
    "super": "super user permissions",
}
update_oauth2_bearer_scopes(app_scopes)

################################################################################
# SessionMiddleware is needed to check the "state" variable when logging in
# https://auth0.com/docs/secure/attack-protection/state-parameters
middleware = []

middleware.append(
    Middleware(
        SessionMiddleware,
        https_only=True,
        max_age=None,
        same_site="strict",
        secret_key=os.urandom(32),
    )
)

################################################################################
swagger_ui_init_oauth = {}

if settings.DEVEL_ENVIRONMENT:
    # save some time copy/pasting id/secret when using swagger_ui
    swagger_ui_init_oauth = {
        "clientId": auth0_settings.AUTH0_CLIENT_ID,
        "clientSecret": auth0_settings.AUTH0_CLIENT_SECRET,
        "scopes": "openid email profile",
    }

app = FastAPI(
    middleware=middleware,
    swagger_ui_init_oauth=swagger_ui_init_oauth,
)

################################################################################
# add the default fastapi_auth0_code_flow router/endpoints
# login, logout, userinfo, etc
app.include_router(auth0_api_router, prefix=f"/{auth0_settings.AUTH0_ENDPOINT_PREFIX}")


################################################################################
################################################################################
################################################################################
# example endpoints using fastapi_auth0_code_flow.dependencies
@app.get("/current_token", response_model=JSONWebTokenPayload)
async def get_current_token(
    jwt: JSONWebTokenPayload = Depends(validate_token),
) -> JSONWebTokenPayload:
    """valid JWT; return JWT Payload"""
    return jwt


@app.get("/current_user", response_model=User)
async def get_current_user(
    current_user: User = Depends(current_user),
) -> User:
    """valid JWT; return user info"""
    return current_user


@app.get("/super_secret", dependencies=[Depends(ValidateScopes(["super"]))])
async def get_super_secret():
    """require a specific set of scopes (e.g. ["super"] for this endpoint)"""
    return {"super_secret": "please don't tell anyone else!"}


################################################################################
################################################################################
################################################################################
@app.on_event("startup")
def enable_fastapi_auth0_code_flow_logs():
    import logging
    from fastapi_auth0_code_flow.logger import logger

    log_level = logging.ERROR
    if settings.DEVEL_ENVIRONMENT:
        log_level = logging.DEBUG

    logger.setLevel(log_level)
    logger.addHandler(logging.StreamHandler())


################################################################################
################################################################################
################################################################################
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=str(settings.UVICORN_HOST),
        port=int(settings.UVICORN_PORT),
        reload=bool(settings.UVICORN_RELOAD),
    )
