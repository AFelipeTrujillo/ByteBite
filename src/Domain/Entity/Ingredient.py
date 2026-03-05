from dataclasses import dataclass
from uuid import UUID

from src.Domain.ValueObject.Category import Category


@dataclass
class Ingredient:
    id: UUID
    name: str
    category: Category