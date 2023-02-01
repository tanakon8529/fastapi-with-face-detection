from __future__ import annotations

from fastapi import HTTPException
from typing import Any
from loguru import logger

from app.apis.face_detection.submod import face_detection_process

def get_face_detection():
    try:
        result = face_detection_process()
        if result == None:
            raise HTTPException(status_code=404, detail='Not Found')
        
        if "error_code" in result:
            if result["error_code"] == "16":
                raise HTTPException(status_code=502, detail='{}'.format(result["msg"]))
            raise HTTPException(status_code=400, detail='{}'.format(result["msg"]))
        
        if "errorCode" in result:
            raise HTTPException(status_code=400, detail=result)

        return result
    except Exception as e:
        logger.error(f"{e}")
        if isinstance(e, HTTPException):
            raise
        else:
            raise HTTPException(status_code=500, detail='internal server error: {0}'.format(e))
