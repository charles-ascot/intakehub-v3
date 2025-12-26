"""Routes for credentials"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_credentials():
    return {"message": "credentials endpoint"}
