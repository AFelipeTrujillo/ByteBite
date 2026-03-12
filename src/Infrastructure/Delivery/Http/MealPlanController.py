from fastapi import APIRouter, Depends, status
from uuid import UUID
from src.Application.UseCase.CreateMealPlan import CreateMealPlan
from src.Infrastructure.Delivery.Http.Schemas.MealPlanSchema import CreateMealPlanRequest
from src.Infrastructure.DependencyInjection.MongoProviders import get_create_meal_plan_use_case
from src.Infrastructure.Security.AuthService import get_current_user_id

router = APIRouter()


@router.post("/meal-plans", status_code=status.HTTP_201_CREATED)
async def create_meal_plan(
        request: CreateMealPlanRequest,
        current_user_id: UUID = Depends(get_current_user_id),
        use_case: CreateMealPlan = Depends(get_create_meal_plan_use_case)
):

    plan_id = await use_case.execute(
        owner_id=current_user_id,
        year=request.year,
        week_number=request.week_number,
        days_data=request.days
    )

    return {"id": plan_id, "status": "created"}