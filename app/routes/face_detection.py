from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile
from app.core.auth import verify_token_user_info
from app.utils.face_detection_engine import face_detect, render
from loguru import logger

import argparse

router = APIRouter()

@router.post("/v1/")
async def face_detection(
    image: UploadFile,
    dev_user_info: Depends = Depends(verify_token_user_info)
):
    # parsing arguments
    parser = argparse.ArgumentParser(description='Simple Face Detection.')
    parser.add_argument("-s", "--source",
                        type=str,
                        default="0",
                        help="Source. Path to the input image.")

    parser.add_argument("-m", "--model",
                       type=str,
                       default="haarcascade_frontalface_default.xml",
                       help="Model path. Path to the 'haarcascade_frontalface_default.xml'.")

    parser.add_argument("-u", "--nogui",
                        type=bool,
                        default=False,
                        help="Enable GUI?. Disable GUI. Default False.")

    args = parser.parse_args()
    logger.info("Using model", args.model)

    detected_faces = face_detect(image, cascasdepath=args.model)
    n_faces = render(image, detected_faces, nogui=False)

    return {
        "detected_faces" : detected_faces,
        "n_faces" : n_faces
    }