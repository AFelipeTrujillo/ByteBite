from dataclasses import dataclass, field
from uuid import UUID
from typing import List
from src.Domain.ValueObject.Unit import Unit
from src.Domain.ValueObject.Category import Category


@dataclass(frozen=True)
class ShoppingListItemDTO:
    ingredient_id: UUID
    ingredient_name: str
    amount: float
    unit: Unit
    category: Category
    checked: bool = False


@dataclass(frozen=True)
class CategoryGroupDTO:
    category: str
    items: List[ShoppingListItemDTO]


@dataclass(frozen=True)
class ShoppingListGroupedDTO:
    meal_plan_id: UUID
    categories: List[CategoryGroupDTO]
