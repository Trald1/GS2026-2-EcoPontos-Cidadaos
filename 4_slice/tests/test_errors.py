def test_validation_error_standardized(client):
    response = client.get("/points?limit=0")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_semantically_blank_question(client):
    response = client.post("/ask", json={"point_id": "eco-001", "question": "   "})
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "BAD_REQUEST"


def test_reject_extra_payload_keys(client):
    response = client.post("/ask", json={"point_id": "eco-001", "question": "Papel?",
                                         "secret": "not allowed"})
    assert response.status_code == 422
