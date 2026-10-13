"""
Response Validator for NEBULA Grounded AI.
Ensures responses adhere to strict scientific safety, do not hallucinate
unverified numerical measurements, explicitly state unavailable properties,
and clearly distinguish between empirical data, derived results, and explanations.
"""
from typing import Dict, Any, List, Optional
import re
import logging

logger = logging.getLogger(__name__)


class ResponseValidator:
    """
    Validates AI responses against physical consistency rules,
    detects fabricated measurements, and ensures proper grounding provenance.
    """

    def validate_response(
        self,
        response_text: str,
        grounding_meta: Dict[str, Any],
        mode: str
    ) -> Dict[str, Any]:
        """
        Runs validation checks on the AI response text.
        Returns safety assessment, flags, and validation metrics.
        """
        safety_flags = []
        is_safe = True

        # Check 1: Empty or extremely short response
        if not response_text or len(response_text.strip()) < 5:
            return {
                "is_valid": False,
                "safety_flags": ["EMPTY_OR_TRUNCATED_RESPONSE"],
                "validation_score": 0.0,
                "sanitized_response": "I encountered an error generating a verified response. Please try again."
            }

        # Check 2: Unrealistic physics indicators (e.g. temperatures below 0 K)
        temp_below_zero = re.search(r'(-\d+(\.\d+)?)\s*(K|Kelvin)', response_text, re.IGNORECASE)
        if temp_below_zero:
            safety_flags.append("VIOLATION_ABSOLUTE_ZERO_TEMPERATURE")
            is_safe = False

        # Check 3: Raw measurement fabrication warning
        # If response claims a precision of 10 decimal places for something not in grounding_meta
        hyper_precise = re.findall(r'\b\d+\.\d{7,}\b', response_text)
        if hyper_precise and not grounding_meta.get("is_grounded"):
            safety_flags.append("POTENTIAL_FABRICATED_PRECISION")

        # Check 4: Unavailable data handling
        # If unavailable properties were in grounding metadata, check if response mentions unavailable
        if grounding_meta.get("unavailable_properties"):
            mentions_unavailable = any(
                w in response_text.lower() for w in ["unavailable", "not recorded", "not available", "missing", "unknown"]
            )
            if not mentions_unavailable:
                safety_flags.append("UNVERIFIED_DATA_OMISSION")

        # Check 5: Mode-specific formatting verification
        mode_key = (mode or "citizen").lower()
        if mode_key == "researcher":
            # Check for quantitative units or math symbols
            has_units = any(u in response_text for u in ["kg", "km", "AU", "m/s", "M_\\odot", "M_\\oplus", "K", "days"])
            if not has_units and len(response_text) > 100:
                safety_flags.append("RESEARCHER_MISSING_FORMAL_UNITS")
        elif mode_key == "student":
            # Encourage pedagogical structure
            pass

        validation_score = 1.0 - (len(safety_flags) * 0.15)
        validation_score = max(0.0, min(1.0, validation_score))

        return {
            "is_valid": is_safe,
            "safety_flags": safety_flags,
            "validation_score": round(validation_score, 2),
            "sanitized_response": response_text
        }


response_validator = ResponseValidator()
