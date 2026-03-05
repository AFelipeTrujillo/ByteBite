from dataclasses import dataclass, field
from typing import Optional, Dict
from uuid import UUID

@dataclass
class DailyPlan:
    lunch_recipe_id: Optional[UUID] = None
    dinner_recipe_id: Optional[UUID] = None

@dataclass
class MealPlan:
    id: UUID
    owner_id: UUID
    year: int
    week_number: int
    days: Dict[int, DailyPlan] = field(default_factory=dict)