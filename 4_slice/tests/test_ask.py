from fastapi.testclient import TestClient

from src.api.app import create_app
from src.domain.service import CitizenService
from src.infra.repository import InMemoryPointRepository


class StubProvider:
    def __init__(self, intent="supported", fail=False):
        self.intent = intent
        self.fail = fail
        self.calls = 0

    def classify(self, point, question):
        self.calls += 1
        if self.fail:
            raise RuntimeError("simulação de indisponibilidade")
        return self.intent


def test_ask_happy_with_fake_adapter():
    fake = StubProvider()
    client = TestClient(create_app(CitizenService(InMemoryPointRepository(), fake)))
    response = client.post("/ask", json={"point_id": "eco-001", "question": "Aceita papel?"})
    assert response.status_code == 200
    assert response.json()["status"] == "answered"
    assert "papel" in response.json()["answer"]
    assert fake.calls == 1


def test_ask_out_of_scope_never_calls_provider():
    fake = StubProvider()
    client = TestClient(create_app(CitizenService(InMemoryPointRepository(), fake)))
    response = client.post("/ask", json={"point_id": "eco-001", "question": "Quem ganhou?"})
    assert response.status_code == 200
    assert response.json()["status"] == "refused"
    assert fake.calls == 0


def test_ask_provider_refusal():
    client = TestClient(create_app(CitizenService(InMemoryPointRepository(),
                                                 StubProvider(intent="unknown"))))
    response = client.post("/ask", json={"point_id": "eco-001", "question": "Descartar?"})
    assert response.status_code == 200
    assert response.json()["status"] == "refused"


def test_ask_provider_down():
    client = TestClient(create_app(CitizenService(InMemoryPointRepository(),
                                                 StubProvider(fail=True))))
    response = client.post("/ask", json={"point_id": "eco-001", "question": "Reciclar?"})
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "AI_UNAVAILABLE"


def test_ask_unknown_point(client):
    response = client.post("/ask", json={"point_id": "unknown", "question": "Aceita vidro?"})
    assert response.status_code == 404


def test_special_waste_refused_without_provider():
    fake = StubProvider()
    client = TestClient(create_app(CitizenService(InMemoryPointRepository(), fake)))
    response = client.post("/ask", json={"point_id": "eco-001",
                                         "question": "Onde descartar baterias?"})
    assert response.status_code == 200
    assert response.json()["status"] == "refused"
    assert fake.calls == 0
