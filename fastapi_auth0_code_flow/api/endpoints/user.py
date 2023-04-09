from fastapi import APIRouter, Depends

from fastapi_auth0_code_flow import schemas
from fastapi_auth0_code_flow.dependencies import current_user

router = APIRouter(tags=["user"])


@router.get("/me/info", response_model=schemas.User)
async def get_current_user_information(
    current_user=Depends(current_user),
) -> schemas.User:
    """
    returns result from <auth0.com>/userinfo

    https://auth0.com/docs/api/authentication#user-profile
    """
    return current_user
