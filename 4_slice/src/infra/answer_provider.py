from src.domain.models import Point


class FakeAnswerProvider:
    """Fake determinístico. Não conecta a LLM externa e não gera novos fatos."""

    def classify(self, point: Point, question: str) -> str:
        del point, question
        return "supported"
