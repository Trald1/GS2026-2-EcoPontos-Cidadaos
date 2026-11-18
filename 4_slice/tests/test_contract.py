from pathlib import Path

import jsonschema
import yaml
from fastapi.testclient import TestClient

from src.api.app import app

SPEC = Path(__file__).resolve().parents[2] / "2_contrato_api.yaml"


def get_schema(name):
    spec = yaml.safe_load(SPEC.read_text(encoding="utf-8"))
    schema = spec["components"]["schemas"][name]
    resolver = jsonschema.RefResolver.from_schema(spec)
    return schema, resolver


def test_contract_paths_and_version():
    spec = yaml.safe_load(SPEC.read_text(encoding="utf-8"))
    assert spec["openapi"] == "3.0.3"
    assert set(spec["paths"]) == {"/points", "/points/{id}", "/ask"}
    for operation in (spec["paths"]["/points"]["get"],
                      spec["paths"]["/points/{id}"]["get"],
                      spec["paths"]["/ask"]["post"]):
        assert "422" in operation["responses"]


def test_contract_response_matches_yaml():
    client = TestClient(app)
    samples = [
        ("PointPage", client.get("/points")),
        ("Point", client.get("/points/eco-001")),
        ("AskResponse", client.post("/ask", json={"point_id": "eco-001",
                                                  "question": "Aceita papel?"})),
        ("ErrorResponse", client.get("/points/eco-unknown")),
        ("ErrorResponse", client.get("/points?limit=0")),
    ]
    for name, response in samples:
        schema, resolver = get_schema(name)
        jsonschema.validate(instance=response.json(), schema=schema, resolver=resolver)
