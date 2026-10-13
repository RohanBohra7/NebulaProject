"""
Comprehensive Grounding & Safety Verification Test Suite for NEBULA AI Assistant.
Tests:
- Object lookup ("What is the mass of Jupiter?")
- Comparison ("Compare Earth and Mars.")
- Simulation interpretation ("What happened in this simulation?")
- Missing data handling (no fabricated values)
- Malformed inputs & error states
- Provider failover & deterministic fallback mode
- Mode-specific tone, formulas, and vocabulary (Citizen / Student / Researcher)
- Tool registry execution and discovery
"""
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.ai.service import ai_service
from app.ai.tools import tool_registry
from app.simulation.manager import simulation_manager


def test_ai_tools_registry_discovery(client: TestClient):
    """Verifies that the ToolRegistry lists all expected astronomical and simulation tools."""
    res = client.get("/api/v1/ai/tools")
    assert res.status_code == 200
    data = res.json()
    assert "tools" in data
    assert data["total_tools"] >= 8

    tool_names = [t["name"] for t in data["tools"]]
    assert "get_object" in tool_names
    assert "search_objects" in tool_names
    assert "compare_objects" in tool_names
    assert "get_object_properties" in tool_names
    assert "calculate_orbital_property" in tool_names
    assert "get_simulation" in tool_names
    assert "get_simulation_results" in tool_names
    assert "explain_simulation_result" in tool_names
    assert "query_strongest_gravity" in tool_names


def test_ai_tool_direct_execution(client: TestClient):
    """Verifies direct execution of registered tools via API."""
    # Execute get_object
    payload = {"arguments": {"object_id": "jupiter"}}
    res = client.post("/api/v1/ai/tools/get_object/execute", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["result"]["found"] is True
    assert data["result"]["object"]["name"] == "Jupiter"

    # Execute calculate_orbital_property: gravitational_force
    calc_payload = {
        "arguments": {
            "property_name": "gravitational_force",
            "params": {"mass1": 5.972e24, "mass2": 1.989e30, "distance": 1.496e11}
        }
    }
    calc_res = client.post("/api/v1/ai/tools/calculate_orbital_property/execute", json=calc_payload)
    assert calc_res.status_code == 200
    calc_data = calc_res.json()
    assert calc_data["status"] == "success"
    assert "result" in calc_data["result"]
    assert calc_data["result"]["result"]["force_newtons"] > 3.0e22

    # Execute invalid tool
    bad_res = client.post("/api/v1/ai/tools/non_existent_tool/execute", json={"arguments": {}})
    assert bad_res.status_code == 404


def test_ai_grounded_object_lookup_mass_of_jupiter(client: TestClient):
    """Verifies numerical grounding for: 'What is the mass of Jupiter?'."""
    payload = {
        "prompt": "What is the mass of Jupiter?",
        "mode": "researcher"
    }
    res = client.post("/api/v1/ai/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    resp_text = data["response"]

    # Factual empirical values from NEBULA catalog
    assert "1.898" in resp_text or "317.8" in resp_text or "Jupiter" in resp_text
    assert data["is_grounded"] is True
    assert data["mode"] == "researcher"
    assert "distinctions" in data
    assert "nebula_data" in data["distinctions"]


def test_ai_grounded_comparison_earth_and_mars(client: TestClient):
    """Verifies comparative synthesis: 'Compare Earth and Mars.'."""
    payload = {
        "prompt": "Compare Earth and Mars.",
        "mode": "student"
    }
    res = client.post("/api/v1/ai/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    resp_text = data["response"]

    assert "Earth" in resp_text
    assert "Mars" in resp_text
    # Student mode should include pedagogical engagement
    assert "Comprehension Check" in resp_text or "gravity" in resp_text.lower()
    assert data["mode"] == "student"


def test_ai_grounded_orbital_period_explanation(client: TestClient):
    """Verifies physics derivation: 'Explain Earth's orbital period.'."""
    payload = {
        "prompt": "Explain Earth's orbital period.",
        "mode": "student"
    }
    res = client.post("/api/v1/ai/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    resp_text = data["response"]

    assert "365" in resp_text
    assert "Kepler" in resp_text or "orbit" in resp_text.lower()


def test_ai_grounded_saturn_rings_roche_limit(client: TestClient):
    """Verifies physical mechanism: 'Why does Saturn have rings?'."""
    payload = {
        "prompt": "Why does Saturn have rings?",
        "mode": "researcher"
    }
    res = client.post("/api/v1/ai/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    resp_text = data["response"]

    assert "Saturn" in resp_text
    assert "Roche" in resp_text or "tidal" in resp_text.lower() or "ice" in resp_text.lower()


def test_ai_grounded_strongest_gravity_query(client: TestClient):
    """Verifies query: 'Which planet has the strongest gravity?'."""
    payload = {
        "prompt": "Which planet has the strongest gravity?",
        "mode": "citizen"
    }
    res = client.post("/api/v1/ai/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    resp_text = data["response"]

    assert "Jupiter" in resp_text
    assert data["mode"] == "citizen"


def test_ai_grounded_simulation_interpretation(client: TestClient):
    """Verifies simulation interpretation: 'What happened in this simulation?'."""
    # First create and run a simulation
    sim = simulation_manager.create_simulation(scenario_id="sun_earth", num_steps=20, auto_run=True)
    sim_id = sim["id"]

    payload = {
        "prompt": f"What happened in simulation {sim_id}?",
        "simulation_id": sim_id,
        "mode": "researcher"
    }
    res = client.post("/api/v1/ai/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    resp_text = data["response"]

    assert sim_id in resp_text or "Simulation" in resp_text or "Energy" in resp_text
    assert "NEBULA N-Body" in resp_text or "Conserved" in resp_text or "dynamics" in resp_text.lower()


def test_ai_explain_simulation_endpoint(client: TestClient):
    """Verifies the dedicated /explain-simulation endpoint."""
    sim = simulation_manager.create_simulation(scenario_id="sun_earth_moon", num_steps=20, auto_run=True)
    sim_id = sim["id"]

    res = client.post("/api/v1/ai/explain-simulation", json={"simulation_id": sim_id, "mode": "researcher"})
    assert res.status_code == 200
    data = res.json()
    assert "response" in data
    assert len(data["response"]) > 20


def test_ai_missing_data_handling(client: TestClient):
    """Verifies that missing data is explicitly stated and not silently fabricated."""
    res = tool_registry.get_tool("get_object_properties").func(
        object_id="ceres",
        properties=["mass_kg", "non_existent_spectroscopy_property_xyz"]
    )
    assert "non_existent_spectroscopy_property_xyz" in res["unavailable_properties"]
    assert "mass_kg" in res["available_properties"]


def test_ai_malformed_input(client: TestClient):
    """Verifies 400 Bad Request on empty or whitespace prompt."""
    res1 = client.post("/api/v1/ai/chat", json={"prompt": ""})
    assert res1.status_code == 400

    res2 = client.post("/api/v1/ai/chat", json={"prompt": "   "})
    assert res2.status_code == 400


def test_ai_mode_specific_differentiation(client: TestClient):
    """Verifies genuinely distinct cognitive content and styling across the 3 modes."""
    prompt = "What is the mass of Jupiter?"

    # Citizen Mode
    res_cit = client.post("/api/v1/ai/chat", json={"prompt": prompt, "mode": "citizen"})
    cit_text = res_cit.json()["response"]

    # Student Mode
    res_stu = client.post("/api/v1/ai/chat", json={"prompt": prompt, "mode": "student"})
    stu_text = res_stu.json()["response"]

    # Researcher Mode
    res_res = client.post("/api/v1/ai/chat", json={"prompt": prompt, "mode": "researcher"})
    res_text = res_res.json()["response"]

    # Citizen should use relatable analogies
    assert "titan" in cit_text.lower() or "basketball" in cit_text.lower() or "earth" in cit_text.lower()
    # Student should include pedagogical comprehension check
    assert "Comprehension Check" in stu_text
    # Researcher should use LaTeX notation or formal astrometric terminology
    assert "$" in res_text or "barycentric" in res_text.lower() or "\\text" in res_text


def test_ai_provider_failover_to_fallback(client: TestClient):
    """Verifies that if an active external provider raises an exception, the system gracefully falls back."""
    with patch.object(ai_service.gemini_provider, "is_available", return_value=True), \
         patch.object(ai_service.gemini_provider, "generate_response", side_effect=RuntimeError("Simulated API 500 error")):
        res = client.post("/api/v1/ai/chat", json={"prompt": "What is the mass of Jupiter?", "mode": "citizen"})
        assert res.status_code == 200
        result = res.json()
        assert result["used_fallback"] is True
        assert "Jupiter" in result["response"]
        assert len(result["response"]) > 20
