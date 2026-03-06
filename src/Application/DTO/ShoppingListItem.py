from dataclasses import dataclass
from uuid import UUID
from src.Domain.ValueObject.Unit import Unit

@dataclass(frozen=True)
class ShoppingListItemDTO:
    ingredient_id: UUID
    ingredient_name: str
    amount: float
    unit: Unit