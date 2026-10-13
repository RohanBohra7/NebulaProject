from pydantic_settings import BaseSettings
from typing import Optional, List
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "NEBULA: Intelligent Astronomical Data Platform"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    API_LEGACY_STR: str = "/api"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]
    
    # Database
    DATABASE_URL: str = "sqlite:///./nebula.db"
    
    # AI Keys (provider-agnostic)
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    OLLAMA_BASE_URL: Optional[str] = "http://localhost:11434"
    DEFAULT_AI_PROVIDER: str = "auto"  # auto | gemini | openai | anthropic | ollama | fallback
    
    # Simulation defaults
    DEFAULT_INTEGRATOR: str = "ias15"  # ias15 | whfast | leapfrog | rk4
    
    # Data seed path
    DATA_SEED_PATH: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "data",
        "seed_astronomical_data.json"
    )
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
