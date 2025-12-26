"""Routes for monitoring"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_monitoring():
    return {"message": "monitoring endpoint"}
