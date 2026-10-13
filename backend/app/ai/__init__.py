"""
NEBULA Grounded AI Assistant Package.
Exports core architecture classes:
- AIService
- AIProvider
- ContextBuilder
- ToolRegistry
- PromptManager
- ResponseValidator
"""

from app.ai.service import AIService, ai_service
from app.ai.providers import (
    AIProvider,
    GeminiProvider,
    OpenAIProvider,
    LocalDeterministicProvider
)
from app.ai.tools import ToolRegistry, tool_registry
from app.ai.context_builder import ContextBuilder, context_builder
from app.ai.prompt_manager import PromptManager, prompt_manager
from app.ai.response_validator import ResponseValidator, response_validator

__all__ = [
    "AIService",
    "ai_service",
    "AIProvider",
    "GeminiProvider",
    "OpenAIProvider",
    "LocalDeterministicProvider",
    "ToolRegistry",
    "tool_registry",
    "ContextBuilder",
    "context_builder",
    "PromptManager",
    "prompt_manager",
    "ResponseValidator",
    "response_validator"
]
