from uuid import UUID, uuid4
from typing import Dict
from src.Domain.Entity.MealPlan import MealPlan, DailyPlan
from src.Domain.Repository.MealPlanRepository import MealPlanRepository

class CreateMealPlan:
    def __init__(self, meal_plan_repo: MealPlanRepository):
        self.meal_plan_repo = meal_plan_repo

    async def execute(
        self,
        owner_id: UUID,
        year: int,
        week_number: int,
        days_data: Dict[int, Dict]
    ) -> UUID:
        days_dict = {}
        for day_index, plan_info in days_data.items():
            days_dict[int(day_index)] = DailyPlan(
                lunch_recipe_id=plan_info.get("lunch_recipe_id"),
                dinner_recipe_id=plan_info.get("dinner_recipe_id")
            )

        meal_plan = MealPlan(
            id=uuid4(),
            owner_id=owner_id,
            year=year,
            week_number=week_number,
            days=days_dict
        )

        await self.meal_plan_repo.save(meal_plan)

        return meal_plan.id