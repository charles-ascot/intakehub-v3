"""Routes for testing"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_testing():
    return {"message": "testing endpoint"}
