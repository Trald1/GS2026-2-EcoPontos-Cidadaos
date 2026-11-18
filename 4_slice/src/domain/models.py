from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Point:
    id: str
    name: str
    address: str
    materials: tuple[str, ...]
    instructions: str
    updated_at: date
