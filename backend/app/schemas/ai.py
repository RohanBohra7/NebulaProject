from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="User question or inquiry")
    mode: str = Field("citizen", description="Persona mode: researcher | student | citizen")
    target_object_id: Optional[str] = None
    history: Optional[List[Dict[str, str]]] = None

class ExplainObjectRequest(BaseModel):
    object_id: str
    mode: str = Field("citizen", description="Persona mode: researcher | student | citizen")

class AIChatResponseSchema(BaseModel):
    response: str
    mode: str
    provider: str
    grounding_data_used: Dict[str, Any]
    tokens_estimated: Optional[int] = None
    latency_ms: Optional[float] = None
