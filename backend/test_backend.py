import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_tests():
    print(">>> Testing NEBULA Backend Subsystems...")

    # 1. Test database & catalog init
    print("1. Testing database initialization & catalog seeding...")
    from app.data.catalog import init_catalog_db, get_all_objects, get_object_by_id
    from app.db.database import SessionLocal
    init_catalog_db()
    db = SessionLocal()
    objects = get_all_objects(db)
    print(f"   Success: {len(objects)} objects in catalog.")
    earth = get_object_by_id(db, "earth")
    assert earth is not None
    assert earth["name"] == "Earth"
    print(f"   Success: Earth verified (mass={earth['mass_kg']} kg, a={earth['semi_major_axis_au']} AU)")
    db.close()

    # 2. Test orbital mechanics calculations
    print("2. Testing orbital mechanics calculations...")
    from app.computation.orbital_mechanics import (
        solve_kepler,
        orbital_elements_to_cartesian,
        calculate_hohmann_transfer,
        calculate_hill_sphere,
        calculate_roche_limit,
        find_orbital_resonances
    )
    # Kepler solver test
    E = solve_kepler(0.5, 0.2)
    assert abs(E - 0.2 * math.sin(E) - 0.5) < 1e-10
    print(f"   Success: Kepler solver converged (E={round(E, 6)})")

    # Hohmann transfer: Earth to Mars (1.0 AU to 1.524 AU)
    hohmann = calculate_hohmann_transfer(1.0, 1.524)
    print(f"   Success: Earth-Mars Hohmann transfer total dV = {hohmann['total_delta_v_km_s']} km/s, time = {hohmann['transfer_time_days']} days")
    assert 5.0 < hohmann['total_delta_v_km_s'] < 6.5
    assert 240 < hohmann['transfer_time_days'] < 280

    # Hill sphere for Earth
    hill = calculate_hill_sphere(1.0, 0.0167, 5.9722e24)
    print(f"   Success: Earth Hill sphere radius = {hill['hill_radius_km']} km (~1.5 million km)")
    assert 1400000 < hill['hill_radius_km'] < 1600000

    # Resonances test: Neptune & Pluto (~60189 d vs ~90560 d)
    res = find_orbital_resonances(60189.0, 90560.0)
    print(f"   Success: Orbital resonances detected: {[r['ratio_str'] for r in res]}")
    assert any(r["ratio_str"] == "3:2" for r in res)

    # 3. Test N-body simulation
    print("3. Testing N-Body simulation engine...")
    from app.simulation.nbody_engine import simulate_scenario
    sim_result = simulate_scenario("solar_system_inner", integrator="ias15", total_time_years=0.5, num_steps=50)
    print(f"   Success: Solar system simulation completed in {sim_result['runtime_ms']} ms using {sim_result['engine_used']}")
    print(f"   Max energy error dE/E: {sim_result['max_energy_error']:.6e}")
    assert len(sim_result["bodies"]) == 5
    assert len(sim_result["bodies"][0]["trajectory"]) == 51

    # Figure 8 choreography test
    fig8 = simulate_scenario("figure_eight_choreography", total_time_years=0.5, num_steps=50)
    print(f"   Success: Figure-8 choreography simulated. Max dE/E = {fig8['max_energy_error']:.6e}")

    # 4. Test AI grounding & fallback engine
    print("4. Testing Grounded AI service...")
    import asyncio
    from app.ai.service import ai_service
    async def test_ai():
        res_researcher = await ai_service.chat("Explain the gravitational properties of Jupiter", mode="researcher")
        print(f"   Success: Researcher response generated ({len(res_researcher['response'])} chars, provider: {res_researcher['provider']})")
        assert "1.8982" in res_researcher["response"] or "Jupiter" in res_researcher["response"]

        res_citizen = await ai_service.chat("Explain the gravitational properties of Jupiter", mode="citizen")
        print(f"   Success: Citizen response generated ({len(res_citizen['response'])} chars)")
        assert len(res_citizen["response"]) > 50

    asyncio.run(test_ai())

    # 5. Test Research Evaluation framework
    print("5. Testing Research Evaluation multi-persona benchmarks...")
    from app.evaluation.evaluator import evaluate_query_across_modes
    async def test_eval():
        eval_report = await evaluate_query_across_modes("How does TRAPPIST-1e compare to Earth?", target_object_id="trappist-1e")
        print(f"   Success: Evaluation complete.")
        print(f"   Researcher FKGL: {eval_report['researcher']['flesch_kincaid_grade']} | Term density: {eval_report['researcher']['technical_term_density_percent']}%")
        print(f"   Citizen FKGL: {eval_report['citizen']['flesch_kincaid_grade']} | Term density: {eval_report['citizen']['technical_term_density_percent']}%")
        assert eval_report['researcher']['flesch_kincaid_grade'] > eval_report['citizen']['flesch_kincaid_grade']
    
    asyncio.run(test_eval())

    print("\n>>> ALL NEBULA BACKEND SUBSYSTEM TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    import math
    run_tests()
