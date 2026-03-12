from pydantic import BaseModel
from uuid import UUID
from typing import Dict, Optional

class DailyPlanRequest(BaseModel):
    lunch_recipe_id: Optional[UUID] = None
    dinner_recipe_id: Optional[UUID] = None

class CreateMealPlanRequest(BaseModel):
    year: int
    week_number: int
    days: Dict[int, DailyPlanRequest]