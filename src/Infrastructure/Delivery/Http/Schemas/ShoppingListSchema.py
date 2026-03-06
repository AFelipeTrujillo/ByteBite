from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID


class ShoppingListItemResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    ingredient_id: UUID
    ingredient_name: str
    amount: float
    unit: str = Field(..., description="The measurement unit (e.g., g, kg, units)")