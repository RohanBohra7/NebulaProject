from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import (
    NebulaException,
    nebula_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from app.api.v1.router import v1_router
from app.data.catalog import init_catalog_db
from app.simulation.nbody_engine import HAS_REBOUND
from app.ai.service import ai_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure database tables & seed data are initialized
    logger.info("Initializing NEBULA astronomical database and scientific solvers...")
    init_catalog_db()
    logger.info(f"Simulation engine: {'REBOUND IAS15 (C-accelerated)' if HAS_REBOUND else 'NumPy Symplectic Leapfrog'}")
    logger.info(f"AI Knowledge engine: {ai_service.get_active_provider_name()}")
    logger.info("NEBULA backend successfully started. Ready for astronomical exploration.")
    yield
    logger.info("Shutting down NEBULA backend.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Intelligent Astronomical Data Visualization, Simulation, and Multi-Persona Exploration Platform",
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

# Exception handlers
app.add_exception_handler(NebulaException, nebula_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Versioned API: /api/v1
app.include_router(v1_router, prefix=settings.API_V1_STR)

# Mount Legacy/Direct API: /api (backward compatibility for existing endpoints)
app.include_router(v1_router, prefix=settings.API_LEGACY_STR)

@app.get("/")
def root():
    return {
        "platform": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "status": "Online",
        "docs_url": "/docs",
        "api_v1": settings.API_V1_STR,
        "api_health": f"{settings.API_V1_STR}/health",
        "modes": ["researcher", "student", "citizen"]
    }

@app.get("/api/health")
@app.get("/health")
def health():
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
