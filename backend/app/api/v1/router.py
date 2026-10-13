from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.objects import router as objects_router
from app.api.comparison import router as comparison_router
from app.api.calculations import router as calculations_router
from app.api.simulation import router as simulation_router
from app.api.ai import router as ai_router
from app.api.research import router as research_router
from app.api.data_management import router as data_router

v1_router = APIRouter()

# Mount health
v1_router.include_router(health_router)

# Mount domain routers
v1_router.include_router(objects_router)
v1_router.include_router(comparison_router)
v1_router.include_router(calculations_router)
v1_router.include_router(simulation_router)
v1_router.include_router(ai_router)
v1_router.include_router(research_router)
v1_router.include_router(data_router)
