from dataclasses import asdict

from src.domain.ports import AnswerProvider, PointRepository

MATERIALS = ("papel", "plastico", "vidro", "metal")
SPECIAL_WASTE = (
    "bateria",
    "baterias",
    "pilha",
    "pilhas",
    "medicamento",
    "medicamentos",
    "quimico",
    "químico",
    "eletronico",
    "eletrônico",
    "oleo",
    "óleo",
    "lampada",
    "lâmpada",
)
SCOPE_WORDS = (
    "descart",
    "recicl",
    "coleta",
    "ecoponto",
    "material",
    "papel",
    "plastico",
    "plástico",
    "vidro",
    "metal",
    "aceita",
    "recebe",
    "levar",
    "entregar",
)


class NotFound(Exception):
    pass


class BadRequest(Exception):
    pass


class ProviderUnavailable(Exception):
    pass


class CitizenService:
    def __init__(self, repository: PointRepository, provider: AnswerProvider):
        self.repository = repository
        self.provider = provider

    def list_points(self, limit: int, offset: int, material: str | None) -> dict:
        points = self.repository.list_all()
        if material:
            points = [point for point in points if material in point.materials]
        return {
            "items": [asdict(p) for p in points[offset : offset + limit]],
            "total": len(points),
            "limit": limit,
            "offset": offset,
        }

    def get_point(self, point_id: str) -> dict:
        point = self.repository.get(point_id)
        if point is None:
            raise NotFound("Ponto de coleta não encontrado.")
        return asdict(point)

    def ask(self, point_id: str, question: str) -> dict:
        point = self.repository.get(point_id)
        if point is None:
            raise NotFound("Ponto de coleta não encontrado.")
        normalized = question.strip().lower()
        if not normalized:
            raise BadRequest("A pergunta não pode conter apenas espaços.")
        if any(term in normalized for term in SPECIAL_WASTE):
            return {
                "status": "refused",
                "answer": "Não há orientação oficial verificada "
                "para resíduos especiais neste catálogo demonstrativo.",
                "source_point_id": point.id,
                "provider": "fake",
            }
        if not any(term in normalized for term in SCOPE_WORDS):
            return {
                "status": "refused",
                "answer": "Só posso orientar sobre descarte e materiais "
                "cadastrados para este ponto.",
                "source_point_id": point.id,
                "provider": "fake",
            }
        try:
            intent = self.provider.classify(point, normalized)
        except Exception as exc:
            raise ProviderUnavailable("Serviço de orientação indisponível.") from exc
        # O adaptador não controla fatos publicados: resposta final é construída com dados locais.
        if intent != "supported":
            return {
                "status": "refused",
                "answer": "Não há informação suficiente no cadastro para responder com segurança.",
                "source_point_id": point.id,
                "provider": "fake",
            }
        materials = ", ".join(point.materials)
        answer = (
            f"O ponto {point.name} recebe: {materials}. "
            f"Orientação cadastrada: {point.instructions} "
            "Os dados são fictícios e não representam um serviço público real."
        )
        return {
            "status": "answered",
            "answer": answer,
            "source_point_id": point.id,
            "provider": "fake",
        }
