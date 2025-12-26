"""Routes for ingestion"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_ingestion():
    return {"message": "ingestion endpoint"}
