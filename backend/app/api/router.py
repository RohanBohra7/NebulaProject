from fastapi import APIRouter
from app.api.v1.router import v1_router

# Root API router that re-exports all endpoints for backward compatibility
api_router = APIRouter()
api_router.include_router(v1_router)
