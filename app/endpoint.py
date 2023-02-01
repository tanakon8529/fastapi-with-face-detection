from fastapi import APIRouter
from app.routes import access, face_detection

api_router = APIRouter()

api_router.include_router(
    access.router, 
    prefix="/access", 
    tags=["access"]
)

api_router.include_router(
    face_detection.router, 
    prefix="/face_detection", 
    tags=["face_detection"]
)
