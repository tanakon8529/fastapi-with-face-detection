from __future__ import annotations

from fastapi import APIRouter, Depends

from app.apis.access.mainmod import access_token
from app.core.auth import verify_user_info, verify_grant_type

router = APIRouter()


@router.get("/oauth/token")
async def generate_access_token(
    grant_type : Depends = Depends(verify_grant_type),
    user_info: Depends = Depends(verify_user_info)
):
    return access_token(grant_type, user_info)
