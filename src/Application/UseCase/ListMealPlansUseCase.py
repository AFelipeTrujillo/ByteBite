from uuid import UUID
from typing import List
from src.Domain.Entity.MealPlan import MealPlan
from src.Domain.Repository.MealPlanRepository import MealPlanRepository


class ListMealPlansUseCase:
    def __init__(self, meal_plan_repo: MealPlanRepository):
        self.meal_plan_repo = meal_plan_repo

    async def execute(self, owner_id: UUID) -> List[MealPlan]:
        return await self.meal_plan_repo.find_by_owner(owner_id)
