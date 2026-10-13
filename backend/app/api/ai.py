"""
API Endpoints for Grounded AI Astronomy Assistant in NEBULA.
Exposes multi-persona chat, tool discovery, direct tool execution,
and specialized explanation endpoints for objects and N-body simulations.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.ai.service import ai_service
from app.data.seed_data import ASTRONOMICAL_CATALOG

router = APIRouter(prefix="/ai", tags=["Grounded AI Assistant"])


class ChatRequest(BaseModel):
    prompt: str = Field(..., description="User question or inquiry")
    mode: str = Field(default="citizen", description="Persona mode: citizen, student, or researcher")
    target_object_id: Optional[str] = Field(default=None, description="Optional target celestial body ID for context grounding")
    simulation_id: Optional[str] = Field(default=None, description="Optional simulation run ID for trajectory/numerical interpretation")
    comparison_ids: Optional[List[str]] = Field(default=None, description="Optional list of body IDs for comparative synthesis")
    history: Optional[List[Dict[str, str]]] = Field(default=None, description="Recent conversation turns")


class ExplainObjectRequest(BaseModel):
    object_id: str
    mode: str = "citizen"


class ExplainSimulationRequest(BaseModel):
    simulation_id: str
    mode: str = "researcher"


class ExecuteToolRequest(BaseModel):
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Arguments to pass to the tool function")


@router.get("/status")
def ai_status():
    """Returns the current active AI provider, tools count, and grounding engine status."""
    return ai_service.get_status()


@router.get("/tools")
def list_ai_tools():
    """Returns the list of all registered AI tools/functions and their schemas."""
    return {
        "tools": ai_service.list_tools(),
        "total_tools": len(ai_service.list_tools())
    }


@router.post("/tools/{tool_name}/execute")
async def execute_tool_endpoint(tool_name: str, req: ExecuteToolRequest):
    """Executes a registered AI tool directly against NEBULA databases/computational engine."""
    result = await ai_service.execute_tool(tool_name, req.arguments)
    if result.get("status") == "error" and "not registered" in result.get("message", ""):
        raise HTTPException(status_code=404, detail=result["message"])
    return result


@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    """
    Submits a user question to the grounded AI service in the designated persona mode.
    Retrieves empirical catalog data, computes orbital properties, or parses simulation results.
    """
    if not req.prompt or not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    result = await ai_service.chat(
        prompt=req.prompt,
        mode=req.mode,
        target_object_id=req.target_object_id,
        simulation_id=req.simulation_id,
        comparison_ids=req.comparison_ids,
        history=req.history
    )
    return result


@router.post("/explain-object")
async def explain_object_endpoint(req: ExplainObjectRequest):
    """Generates an adaptive grounded explanation for a selected astronomical object."""
    target = None
    for obj in ASTRONOMICAL_CATALOG:
        if obj["id"] == req.object_id:
            target = obj
            break

    if not target:
        raise HTTPException(status_code=404, detail=f"Object '{req.object_id}' not found.")

    prompt = f"Provide a complete, insightful overview of {target['name']} highlighting its most notable physical and orbital characteristics."
    result = await ai_service.chat(
        prompt=prompt,
        mode=req.mode,
        target_object_id=req.object_id
    )
    return result


@router.post("/explain-simulation")
async def explain_simulation_endpoint(req: ExplainSimulationRequest):
    """Generates an astrophysical interpretation of an N-body simulation run."""
    prompt = f"Analyze the numerical dynamics, energy conservation, and stability of simulation {req.simulation_id}."
    result = await ai_service.chat(
        prompt=prompt,
        mode=req.mode,
        simulation_id=req.simulation_id
    )
    return result
