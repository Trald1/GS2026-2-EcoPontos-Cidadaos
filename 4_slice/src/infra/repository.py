from datetime import date

from src.domain.models import Point


class InMemoryPointRepository:
    def __init__(self) -> None:
        self._points = [
            Point("eco-001", "Ecoponto Modelo Centro", "Rua Exemplo, 100 — Cidade Fictícia",
                  ("papel", "plastico", "metal"),
                  "Entregue materiais secos, limpos e separados.", date(2026, 11, 1)),
            Point("eco-002", "Ecoponto Modelo Norte", "Avenida Teste, 200 — Cidade Fictícia",
                  ("vidro", "papel"),
                  "Vidros devem estar acondicionados com segurança.", date(2026, 11, 1)),
            Point("eco-003", "Ecoponto Modelo Sul", "Praça Demonstração, 30 — Cidade Fictícia",
                  ("plastico", "metal"),
                  "Leve embalagens vazias e separadas.", date(2026, 11, 1)),
        ]

    def list_all(self) -> list[Point]:
        return list(self._points)

    def get(self, point_id: str) -> Point | None:
        return next((p for p in self._points if p.id == point_id), None)
