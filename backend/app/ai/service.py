"""
Grounded AI Service for NEBULA.
Orchestrates AI providers, tool execution, grounding context extraction,
prompt management, response validation, and automatic deterministic failover.
"""
from typing import Dict, Any, List, Optional
import os
import logging

from app.config import settings
from app.ai.providers import (
    AIProvider,
    GeminiProvider,
    OpenAIProvider,
    LocalDeterministicProvider
)
from app.ai.tools import tool_registry
from app.ai.context_builder import context_builder
from app.ai.prompt_manager import prompt_manager
from app.ai.response_validator import response_validator

logger = logging.getLogger(__name__)


class AIService:
    """
    Central AI orchestration service for NEBULA.
    Guarantees factual accuracy, multi-persona adaptation, and offline safety.
    """

    def __init__(self):
        self.tool_registry = tool_registry
        self.context_builder = context_builder
        self.prompt_manager = prompt_manager
        self.response_validator = response_validator
        self.fallback_provider = LocalDeterministicProvider()

        # Initialize available remote providers if keys exist
        self.gemini_provider = GeminiProvider()
        self.openai_provider = OpenAIProvider()

    def get_active_provider(self) -> AIProvider:
        """Determines the primary active provider based on environment configuration."""
        if self.gemini_provider.is_available():
            return self.gemini_provider
        if self.openai_provider.is_available():
            return self.openai_provider
        return self.fallback_provider

    def get_active_provider_name(self) -> str:
        prov = self.get_active_provider()
        return prov.get_name()

    def is_fallback_active(self) -> bool:
        prov = self.get_active_provider()
        return isinstance(prov, LocalDeterministicProvider)

    def get_status(self) -> Dict[str, Any]:
        """Returns comprehensive status of AI subsystems."""
        active_prov = self.get_active_provider()
        return {
            "active_provider": active_prov.get_name(),
            "is_fallback_active": isinstance(active_prov, LocalDeterministicProvider),
            "is_deterministic_fallback_ready": True,
            "registered_tools_count": len(self.tool_registry.list_tools()),
            "supported_personas": ["researcher", "student", "citizen"],
            "credentials_status": {
                "gemini_configured": self.gemini_provider.is_available(),
                "openai_configured": self.openai_provider.is_available(),
                "offline_safe": True
            }
        }

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Executes a registered tool directly through the tool registry."""
        return await self.tool_registry.execute(tool_name, arguments)

    def list_tools(self) -> List[Dict[str, Any]]:
        """Lists all registered tools."""
        return self.tool_registry.list_tools()

    async def chat(
        self,
        prompt: str,
        mode: str = "citizen",
        target_object_id: Optional[str] = None,
        simulation_id: Optional[str] = None,
        comparison_ids: Optional[List[str]] = None,
        history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Processes a user question through the grounding pipeline:
        1. ContextBuilder detects entities, runs tools, formats facts.
        2. PromptManager builds persona-tailored system prompt.
        3. Invokes active AIProvider (or falls back if unavailable/errors).
        4. ResponseValidator checks for safety & consistency.
        5. Packages structured response with grounding metadata and distinctions.
        """
        mode_key = (mode or "citizen").lower()
        if mode_key not in ["citizen", "student", "researcher"]:
            mode_key = "citizen"

        # Step 1: Context building and tool invocations
        grounded_context, grounding_meta = await self.context_builder.build_context(
            query=prompt,
            target_object_id=target_object_id,
            simulation_id=simulation_id,
            comparison_ids=comparison_ids
        )

        # Step 2: System prompt preparation
        system_prompt = self.prompt_manager.get_system_prompt(mode_key)
        tools_list = self.tool_registry.list_tools()

        # Step 3: Provider invocation with automatic failover
        provider = self.get_active_provider()
        used_fallback = False
        response_text = ""

        try:
            response_text = await provider.generate_response(
                prompt=prompt,
                system_prompt=system_prompt,
                context=grounded_context,
                history=history,
                tools=tools_list,
                mode=mode_key
            )
        except Exception as e:
            logger.warning(f"Active provider ({provider.get_name()}) failed ({e}); switching to deterministic fallback.")
            used_fallback = True

        if used_fallback or not response_text:
            response_text = await self.fallback_provider.generate_response(
                prompt=prompt,
                system_prompt=system_prompt,
                context=grounded_context,
                history=history,
                tools=tools_list,
                mode=mode_key
            )
            provider_name = self.fallback_provider.get_name()
            used_fallback = True
        else:
            provider_name = provider.get_name()
            used_fallback = isinstance(provider, LocalDeterministicProvider)

        # Step 4: Validate response
        val_result = self.response_validator.validate_response(
            response_text=response_text,
            grounding_meta=grounding_meta,
            mode=mode_key
        )

        # Step 5: Format distinctions
        distinctions = {
            "nebula_data": "Verified values from NEBULA catalog (JPL Horizons/Gaia DR3)",
            "computed_result": "Derived via Newtonian/Keplerian mechanics or REBOUND solver",
            "external_scientific_context": "Astrophysical theory, missions (Cassini, Juno), and literature",
            "general_explanation": f"Adaptive conceptual explanation formatted for {mode_key.capitalize()} persona"
        }

        return {
            "response": val_result["sanitized_response"],
            "mode": mode_key,
            "provider": provider_name,
            "used_fallback": used_fallback,
            "is_grounded": grounding_meta.get("is_grounded", False),
            "tools_invoked": grounding_meta.get("tools_invoked", []),
            "grounding_meta": grounding_meta,
            "distinctions": distinctions,
            "validation": {
                "is_valid": val_result["is_valid"],
                "score": val_result["validation_score"],
                "safety_flags": val_result["safety_flags"]
            }
        }


# Singleton service export
ai_service = AIService()
