def test_list_pagination(client):
    response = client.get("/points?limit=2&offset=0")
    assert response.status_code == 200
    assert response.json()["total"] == 3
    assert len(response.json()["items"]) == 2


def test_list_filter_material(client):
    response = client.get("/points?material=papel")
    assert response.status_code == 200
    assert response.json()["total"] == 2
    assert all("papel" in p["materials"] for p in response.json()["items"])


def test_second_page(client):
    response = client.get("/points?limit=2&offset=2")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1
