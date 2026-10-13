# Re-export settings from core.config for backward compatibility
from app.core.config import Settings, settings

__all__ = ["Settings", "settings"]
