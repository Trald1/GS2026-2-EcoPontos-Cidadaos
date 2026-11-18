def test_detail_success(client):
    response = client.get("/points/eco-001")
    assert response.status_code == 200
    assert response.json()["id"] == "eco-001"
    assert response.json()["updated_at"] == "2026-11-01"


def test_detail_not_found(client):
    response = client.get("/points/eco-999")
    assert response.status_code == 404
    assert response.json() == {"error": {"code": "NOT_FOUND",
                                         "message": "Ponto de coleta não encontrado."}}
