from fastapi import APIRouter

from fastapi_auth0_code_flow.api.endpoints import auth0
from fastapi_auth0_code_flow.api.endpoints import user

api_router = APIRouter(tags=["auth0"])
api_router.include_router(auth0.router, prefix="")
api_router.include_router(user.router, prefix="/user")
