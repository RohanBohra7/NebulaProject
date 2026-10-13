import sys
import os
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app

def verify_milestone():
    print("==========================================================")
    print("NEBULA FIRST WORKING MILESTONE VERIFICATION")
    print("==========================================================")
    
    client = TestClient(app)
    
    # 1. Health checks
    print("\n[1/7] Testing Health & Root Endpoints...")
    r_root = client.get("/")
    assert r_root.status_code == 200, f"Root failed: {r_root.status_code}"
    print(f"  [OK] GET / -> {r_root.json()['platform']} v{r_root.json()['version']}")
    
    r_health = client.get("/api/health")
    assert r_health.status_code == 200, f"/api/health failed: {r_health.status_code}"
    print(f"  [OK] GET /api/health -> status: {r_health.json()['status']}")
    
    r_v1_health = client.get("/api/v1/health")
    assert r_v1_health.status_code == 200, f"/api/v1/health failed: {r_v1_health.status_code}"
    print(f"  [OK] GET /api/v1/health -> simulation: {r_v1_health.json()['simulation_engine']}")

    # 2. Celestial Catalog API
    print("\n[2/7] Testing Astronomical Objects API...")
    r_objects = client.get("/api/v1/objects/")
    assert r_objects.status_code == 200
    objs = r_objects.json()
    print(f"  [OK] GET /api/v1/objects/ -> {len(objs)} objects retrieved.")
    assert len(objs) >= 20, "Expected at least 20 seeded objects"
    
    r_earth = client.get("/api/v1/objects/earth")
    assert r_earth.status_code == 200
    earth = r_earth.json()
    print(f"  [OK] GET /api/v1/objects/earth -> {earth['name']} (mass={earth['mass_kg']} kg, 3D orbit points={len(earth.get('orbit_path_3d', []))})")
    assert len(earth.get("orbit_path_3d", [])) > 0

    # 3. Scientific Calculations
    print("\n[3/7] Testing Scientific Orbital Mechanics...")
    r_hohmann = client.post("/api/v1/calculate/hohmann", json={"origin_id": "earth", "target_id": "mars"})
    assert r_hohmann.status_code == 200
    hohmann = r_hohmann.json()
    print(f"  [OK] Hohmann Transfer Earth->Mars: dV={hohmann['total_delta_v_km_s']} km/s, Time={hohmann['transfer_time_days']} days")
    
    r_hill = client.post("/api/v1/calculate/hill-sphere", json={"object_id": "earth"})
    assert r_hill.status_code == 200
    hill = r_hill.json()
    print(f"  [OK] Hill Sphere Earth: R_H={hill['hill_radius_km']} km")

    # 4. N-Body Simulation
    print("\n[4/7] Testing N-Body Gravitational Engine (REBOUND IAS15)...")
    r_sim = client.post("/api/v1/simulation/run", json={
        "scenario_id": "solar_system_inner",
        "integrator": "ias15",
        "total_time_years": 0.5,
        "num_steps": 50
    })
    assert r_sim.status_code == 200
    sim = r_sim.json()
    print(f"  [OK] Simulation executed: {sim['engine_used']} in {sim['runtime_ms']} ms")
    print(f"  [OK] Particle count: {len(sim['bodies'])}, Energy error dE/E: {sim['max_energy_error']:.3e}")

    # 5. Grounded AI Personas
    print("\n[5/7] Testing Grounded AI Personas (Researcher vs Student vs Citizen)...")
    modes = ["researcher", "student", "citizen"]
    for m in modes:
        t0 = time.perf_counter()
        r_ai = client.post("/api/v1/ai/chat", json={
            "prompt": "Explain the gravitational properties of Jupiter",
            "mode": m,
            "target_object_id": "jupiter"
        })
        t1 = time.perf_counter()
        assert r_ai.status_code == 200
        ai_resp = r_ai.json()
        print(f"  [OK] AI [{m.upper()}]: {len(ai_resp['response'])} chars, {round((t1-t0)*1000, 1)} ms, Provider: {ai_resp['provider'][:35]}...")

    # 6. Research Evaluation Metrics
    print("\n[6/7] Testing Multi-Persona Research Benchmark Evaluator...")
    r_eval = client.post("/api/v1/research/evaluate", json={
        "query": "How does TRAPPIST-1e compare to Earth in terms of habitability and gravity?",
        "target_object_id": "trappist-1e"
    })
    assert r_eval.status_code == 200
    ev = r_eval.json()
    print(f"  [OK] Researcher FKGL: {ev['researcher']['flesch_kincaid_grade']} | Term Density: {ev['researcher']['technical_term_density_percent']}%")
    print(f"  [OK] Student FKGL:    {ev['student']['flesch_kincaid_grade']} | Term Density: {ev['student']['technical_term_density_percent']}%")
    print(f"  [OK] Citizen FKGL:    {ev['citizen']['flesch_kincaid_grade']} | Term Density: {ev['citizen']['technical_term_density_percent']}%")
    assert ev['researcher']['flesch_kincaid_grade'] > ev['citizen']['flesch_kincaid_grade']

    # 7. Data Management & Provenance
    print("\n[7/7] Testing Data Management & Provenance...")
    r_data = client.get("/api/v1/data/status")
    assert r_data.status_code == 200
    data_st = r_data.json()
    print(f"  [OK] Data Provenance: {data_st['primary_provenance']}")
    print(f"  [OK] Active Data Sources: {len(data_st['sources'])} registered")

    print("\n==========================================================")
    print("ALL MILESTONE VERIFICATION CHECKS PASSED WITH 100% SUCCESS!")
    print("==========================================================")

if __name__ == "__main__":
    verify_milestone()
