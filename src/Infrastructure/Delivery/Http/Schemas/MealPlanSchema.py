from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Dict, Optional

class DailyPlanRequest(BaseModel):
    lunch_recipe_id: Optional[UUID] = None
    dinner_recipe_id: Optional[UUID] = None

class CreateMealPlanRequest(BaseModel):
    year: int
    week_number: int
    days: Dict[int, DailyPlanRequest]


class DailyPlanResponse(BaseModel):
    lunch_recipe_id: Optional[UUID] = None
    dinner_recipe_id: Optional[UUID] = None

class MealPlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_id: UUID
    year: int
    week_number: int
    days: Dict[int, DailyPlanResponse]
