from pydantic import BaseModel
from uuid import UUID

from src.Domain.ValueObject.Unit import Unit

class ShoppingListItem(BaseModel):
    ingredient_id: UUID
    ingredient_name: str
    amount: float
    unit: Unit
