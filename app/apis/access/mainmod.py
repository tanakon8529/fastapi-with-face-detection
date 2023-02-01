from __future__ import annotations

from fastapi import HTTPException
from typing import Any
from loguru import logger

from app.apis.access.submod import generate_access_token, get_access_token

def access_token(grant_type: str, user_info: Any):

    try:
        if grant_type == "client_credentials":
            result = generate_access_token(user_info)

        elif grant_type == "get_client_credentials":
            result = get_access_token(user_info)

        if result == None:
            raise HTTPException(status_code=503, detail='access_token not found, please generate token')

        return result
    except Exception as e:
        logger.error(f"{e}")
        if isinstance(e, HTTPException):
            raise
        else:
            raise HTTPException(status_code=500, detail='internal server error: {0}'.format(e))
