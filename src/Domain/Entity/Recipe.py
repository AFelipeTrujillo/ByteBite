from dataclasses import dataclass, field
from uuid import UUID
from typing import List

from src.Domain.ValueObject.IngredientQuantity import IngredientQuantity

@dataclass
class RecipeIngredient:
    ingredient_id: UUID
    quantity: IngredientQuantity


@dataclass
class Recipe:
    id: UUID
    owner_id: UUID
    name: str
    ingredients: List[RecipeIngredient]
    references: List[str] = field(default_factory=list)
    invited_users: List[UUID] = field(default_factory=list)