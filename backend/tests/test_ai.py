def test_ai_status(client):
    res = client.get("/api/v1/ai/status")
    assert res.status_code == 200
    data = res.json()
    assert "active_provider" in data
    assert data["is_deterministic_fallback_ready"] is True

def test_ai_chat_researcher_mode(client):
    payload = {
        "prompt": "What are the physical parameters of Jupiter?",
        "mode": "researcher",
        "target_object_id": "jupiter"
    }
    res = client.post("/api/v1/ai/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "Jupiter" in data["response"]
    assert data["mode"] == "researcher"

def test_ai_chat_citizen_mode(client):
    payload = {
        "prompt": "What are the physical parameters of Jupiter?",
        "mode": "citizen",
        "target_object_id": "jupiter"
    }
    res = client.post("/api/v1/ai/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "Jupiter" in data["response"]
    assert data["mode"] == "citizen"
