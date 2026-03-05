from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

from src.Domain.Entity.MealPlan import MealPlan


class MealPlanRepository(ABC):

    @abstractmethod
    async def get_by_id(self, meal_plan_id: UUID) -> Optional[MealPlan]:
        pass

    @abstractmethod
    async def save(self, meal_plan: MealPlan) -> None:
        pass
