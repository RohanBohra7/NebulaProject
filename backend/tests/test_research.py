def test_research_evaluate_endpoint(client):
    payload = {
        "query": "How does TRAPPIST-1e compare to Earth?",
        "target_object_id": "trappist-1e"
    }
    res = client.post("/api/v1/research/evaluate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "researcher" in data
    assert "student" in data
    assert "citizen" in data
    assert data["researcher"]["flesch_kincaid_grade"] > data["citizen"]["flesch_kincaid_grade"]

def test_research_benchmarks(client):
    res = client.get("/api/v1/research/benchmarks")
    assert res.status_code == 200
    data = res.json()
    assert "persona_complexity_benchmarks" in data
    assert "simulation_engine_benchmarks" in data
