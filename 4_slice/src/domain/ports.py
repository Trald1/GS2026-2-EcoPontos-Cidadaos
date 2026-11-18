from typing import Protocol

from src.domain.models import Point


class PointRepository(Protocol):
    def list_all(self) -> list[Point]: ...

    def get(self, point_id: str) -> Point | None: ...


class AnswerProvider(Protocol):
    def classify(self, point: Point, question: str) -> str: ...
