from uuid import UUID
from src.Domain.Entity.MealPlan import MealPlan
from src.Domain.Repository.MealPlanRepository import MealPlanRepository


class GetMealPlanByIdUseCase:
    def __init__(self, meal_plan_repo: MealPlanRepository):
        self.meal_plan_repo = meal_plan_repo

    async def execute(self, meal_plan_id: UUID, user_id: UUID) -> MealPlan:
        meal_plan = await self.meal_plan_repo.get_by_id(meal_plan_id)

        if not meal_plan:
            raise ValueError("Meal plan not found")

        if meal_plan.owner_id != user_id:
            raise PermissionError("You do not have access to this meal plan")

        return meal_plan
