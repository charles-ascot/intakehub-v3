"""Error handling middleware"""
import logging

logger = logging.getLogger(__name__)

async def error_handler_middleware(request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"error": str(e)}
