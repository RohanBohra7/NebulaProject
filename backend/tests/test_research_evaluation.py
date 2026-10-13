"""
Comprehensive Unit and Integration Tests for Phase 9: Research Evaluation and Metrics.
Tests:
- 6 Canonical Predefined Evaluation Tasks
- Task interactive lifecycle (start, complete)
- Server-side automated task execution
- Scientific empirical validation benchmarks with physical tolerances
- Non-sensitive application telemetry ingestion and aggregation
- Privacy compliance and absence of PII
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_predefined_tasks_list():
    """Verifies that all 6 canonical predefined evaluation tasks are listed with full metadata."""
    response = client.get("/api/v1/research/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 6

    task_ids = [t["id"] for t in data]
    assert task_ids == ["task_1", "task_2", "task_3", "task_4", "task_5", "task_6"]

    # Verify task 1 details
    t1 = next(t for t in data if t["id"] == "task_1")
    assert t1["name"] == "Find Earth's Orbital Period"
    assert t1["category"] == "Data Exploration"
    assert "365.256" in t1["expected_value"]
    assert "success_criteria" in t1

    # Verify task 4 details
    t4 = next(t for t in data if t["id"] == "task_4")
    assert t4["name"] == "Run an Earth-Sun Simulation"
    assert t4["category"] == "N-Body Simulation"
    assert "sun_earth" in t4["scenario_id"]


def test_task_interactive_lifecycle():
    """Tests starting and completing an interactive task session."""
    # 1. Start session
    start_resp = client.post("/api/v1/research/tasks/task_1/start")
    assert start_resp.status_code == 200
    session_data = start_resp.json()
    assert "session_id" in session_data
    assert session_data["task_id"] == "task_1"
    assert session_data["status"] == "in_progress"

    # 2. Complete session
    comp_resp = client.post(
        "/api/v1/research/tasks/task_1/complete",
        json={
            "session_id": session_data["session_id"],
            "success": True,
            "duration_ms": 3420.5,
            "metadata": {
                "discovered_value": 365.256,
                "verified_in_ui": True
            }
        }
    )
    assert comp_resp.status_code == 200
    comp_data = comp_resp.json()
    assert comp_data["task_id"] == "task_1"
    assert comp_data["status"] == "completed"
    assert comp_data["success"] is True
    assert comp_data["duration_ms"] > 0


def test_automated_individual_task_execution():
    """Tests automated execution of individual predefined tasks."""
    # Task 1: Find Earth's orbital period
    res1 = client.post("/api/v1/research/tasks/task_1/run_automated")
    assert res1.status_code == 200
    d1 = res1.json()
    assert d1["task_id"] == "task_1"
    assert d1["success"] is True
    assert d1["verification_details"]["check_passed"] is True

    # Task 2: Compare Earth and Mars
    res2 = client.post("/api/v1/research/tasks/task_2/run_automated")
    assert res2.status_code == 200
    d2 = res2.json()
    assert d2["task_id"] == "task_2"
    assert d2["success"] is True
    assert d2["verification_details"]["comparison_payload_valid"] is True

    # Task 3: Locate Jupiter in 3D
    res3 = client.post("/api/v1/research/tasks/task_3/run_automated")
    assert res3.status_code == 200
    d3 = res3.json()
    assert d3["task_id"] == "task_3"
    assert d3["success"] is True

    # Task 4: Run an Earth-Sun simulation
    res4 = client.post("/api/v1/research/tasks/task_4/run_automated")
    assert res4.status_code == 200
    d4 = res4.json()
    assert d4["task_id"] == "task_4"
    assert d4["success"] is True
    assert d4["verification_details"]["steps_computed"] >= 50

    # Task 5: Trajectory interpretation
    res5 = client.post("/api/v1/research/tasks/task_5/run_automated")
    assert res5.status_code == 200
    d5 = res5.json()
    assert d5["task_id"] == "task_5"
    assert d5["success"] is True
    assert d5["verification_details"]["orbital_closure_verified"] is True

    # Task 6: Ask AI to explain orbital period
    res6 = client.post("/api/v1/research/tasks/task_6/run_automated")
    assert res6.status_code == 200
    d6 = res6.json()
    assert d6["task_id"] == "task_6"
    assert d6["success"] is True
    assert d6["verification_details"]["check_passed"] is True


def test_run_all_predefined_tasks_suite():
    """Tests the bulk test runner that executes all 6 tasks in sequence."""
    response = client.post("/api/v1/research/tasks/run_all")
    assert response.status_code == 200
    data = response.json()
    assert data["total_tasks"] == 6
    assert data["passed_tasks"] == 6
    assert data["all_passed"] is True
    assert data["total_execution_ms"] > 0
    assert len(data["results"]) == 6


def test_scientific_validation_benchmarks_suite():
    """
    Tests the empirical scientific validation benchmarks endpoint.
    Verifies that all calculated physical properties fall within explicit tolerances
    against IAU/NASA reference data without fabricated claims.
    """
    response = client.get("/api/v1/research/validation/benchmarks")
    assert response.status_code == 200
    data = response.json()
    assert data["total_benchmarks"] >= 8
    assert data["all_passed"] is True

    benchmarks = data["benchmarks"]
    for b in benchmarks:
        assert "property_name" in b
        assert "category" in b
        assert "formula" in b
        assert "computed_value" in b
        assert "reference_value" in b
        assert "reference_source" in b
        assert "units" in b
        assert "tolerance" in b
        assert "absolute_error" in b
        assert b["passed"] is True
        assert b["absolute_error"] <= b["tolerance"]

    # Specifically check Earth orbital period benchmark
    p_earth = next(b for b in benchmarks if b["id"] == "val_earth_orbital_period")
    assert abs(p_earth["computed_value"] - 365.256) <= p_earth["tolerance"]

    # Specifically check surface gravity benchmarks
    g_earth = next(b for b in benchmarks if b["id"] == "val_earth_surface_gravity")
    assert abs(g_earth["computed_value"] - 9.807) <= g_earth["tolerance"]

    g_jup = next(b for b in benchmarks if b["id"] == "val_jupiter_surface_gravity")
    assert abs(g_jup["computed_value"] - 24.79) <= g_jup["tolerance"]

    # Specifically check N-body conservation
    nbody = next(b for b in benchmarks if b["id"] == "val_nbody_energy_conservation")
    assert nbody["computed_value"] <= nbody["tolerance"]


def test_telemetry_ingestion_and_aggregation():
    """Tests telemetry recording and comprehensive aggregation."""
    # 1. Log various interaction events
    client.post(
        "/api/v1/research/telemetry",
        json={
            "event_type": "visualization_interaction",
            "component": "3d_visualizer",
            "duration_ms": 15.0,
            "success": True,
            "metadata": {"action": "select_body", "body": "jupiter"}
        }
    )
    client.post(
        "/api/v1/research/telemetry",
        json={
            "event_type": "object_discovery",
            "component": "explorer",
            "duration_ms": 42.0,
            "success": True,
            "metadata": {"search_term": "mars", "object_id": "mars"}
        }
    )
    client.post(
        "/api/v1/research/telemetry",
        json={
            "event_type": "page_load",
            "component": "details",
            "duration_ms": 110.0,
            "success": True,
            "metadata": {"route": "/object/earth"}
        }
    )

    # 2. Query summary
    summary_resp = client.get("/api/v1/research/telemetry/summary")
    assert summary_resp.status_code == 200
    summary = summary_resp.json()

    assert summary["total_telemetry_events"] >= 3
    assert "task_completion" in summary
    assert "object_discovery" in summary
    assert "visualization" in summary
    assert "simulation" in summary
    assert "ai_interactions" in summary
    assert "system_performance" in summary
    assert summary["privacy_compliance"]["pii_collected"] is False


def test_telemetry_privacy_preservation():
    """Verifies that PII and sensitive parameters are stripped upon telemetry ingestion."""
    leak_attempt = {
        "event_type": "ui_click",
        "component": "login_modal",
        "duration_ms": 5.0,
        "success": True,
        "metadata": {
            "password": "secretPassword123",
            "token": "bearer_xyz_super_secret",
            "email": "user@example.com",
            "client_ip": "192.168.1.1",
            "safe_action": "click_button"
        }
    }
    resp = client.post("/api/v1/research/telemetry", json=leak_attempt)
    assert resp.status_code == 200
    stored_meta = resp.json()["metadata_json"]

    # Sensitive fields must be stripped
    assert "password" not in stored_meta
    assert "token" not in stored_meta
    assert "email" not in stored_meta
    assert "client_ip" not in stored_meta
    assert stored_meta.get("safe_action") == "click_button"
