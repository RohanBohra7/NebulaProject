from fastapi import APIRouter
from app.core.config import settings
from app.simulation.nbody_engine import HAS_REBOUND
from app.ai.service import ai_service

router = APIRouter(tags=["Health & Status"])

@router.get("/health")
def health_check():
    """System health check and subsystem capability inspection."""
    return {
        "status": "healthy",
        "platform": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "database": "sqlite_ready",
        "simulation_engine": "rebound_ias15_ready" if HAS_REBOUND else "numpy_symplectic_leapfrog_ready",
        "ai_engine": {
            "provider": ai_service.get_active_provider_name(),
            "deterministic_fallback_ready": True
        },
        "supported_modes": ["researcher", "student", "citizen"]
    }
