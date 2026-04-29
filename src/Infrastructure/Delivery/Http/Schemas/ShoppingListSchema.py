from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from typing import List


class ShoppingListItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ingredient_id: UUID
    ingredient_name: str
    amount: float
    unit: str = Field(..., description="The measurement unit (e.g., g, kg, units)")
    category: str = Field(..., description="The ingredient category label (e.g., Vegetables & Greens)")
    checked: bool = False


class CategoryGroupResponse(BaseModel):
    category: str
    items: List[ShoppingListItemResponse]


class ShoppingListGroupedResponse(BaseModel):
    meal_plan_id: UUID
    categories: List[CategoryGroupResponse]
