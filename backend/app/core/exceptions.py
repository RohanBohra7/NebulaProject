from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.logging import logger

class NebulaException(Exception):
    """Base exception for all NEBULA-specific errors."""
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, error_code: str = "NEBULA_ERROR"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)

class AstronomicalObjectNotFoundError(NebulaException):
    def __init__(self, object_id: str):
        super().__init__(
            message=f"Astronomical object with ID '{object_id}' not found in NEBULA catalog.",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="OBJECT_NOT_FOUND"
        )

class ScientificCalculationError(NebulaException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="CALCULATION_ERROR"
        )

class SimulationExecutionError(NebulaException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="SIMULATION_ERROR"
        )

class AIProviderError(NebulaException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_502_BAD_GATEWAY,
            error_code="AI_PROVIDER_ERROR"
        )

# Exception handlers for FastAPI app
async def nebula_exception_handler(request: Request, exc: NebulaException):
    logger.error(f"[{exc.error_code}] {exc.message} (Path: {request.url.path})")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "path": request.url.path
            }
        }
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"[HTTP {exc.status_code}] {exc.detail} (Path: {request.url.path})")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
                "path": request.url.path
            }
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"[VALIDATION_ERROR] {exc.errors()} (Path: {request.url.path})")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request parameters or payload.",
                "details": exc.errors(),
                "path": request.url.path
            }
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    logger.exception(f"[UNHANDLED_EXCEPTION] {str(exc)} (Path: {request.url.path})")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred during astronomical computation.",
                "details": str(exc),
                "path": request.url.path
            }
        }
    )
