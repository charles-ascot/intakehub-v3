"""Routes for health"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_health():
    return {"message": "health endpoint"}
