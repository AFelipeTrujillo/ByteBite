from fastapi import APIRouter, Depends, status, HTTPException
from uuid import UUID
from typing import List
from src.Application.UseCase.CreateMealPlan import CreateMealPlan
from src.Application.UseCase.ListMealPlansUseCase import ListMealPlansUseCase
from src.Application.UseCase.GetMealPlanByIdUseCase import GetMealPlanByIdUseCase
from src.Infrastructure.Delivery.Http.Schemas.MealPlanSchema import CreateMealPlanRequest, MealPlanResponse, DailyPlanResponse
from src.Infrastructure.DependencyInjection.MongoProviders import get_create_meal_plan_use_case, get_list_meal_plans_use_case, get_meal_plan_by_id_use_case
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


@router.get("/meal-plans/{meal_plan_id}", response_model=MealPlanResponse)
async def get_meal_plan_by_id(
        meal_plan_id: UUID,
        current_user_id: UUID = Depends(get_current_user_id),
        use_case: GetMealPlanByIdUseCase = Depends(get_meal_plan_by_id_use_case)
):
    try:
        meal_plan = await use_case.execute(
            meal_plan_id=meal_plan_id,
            user_id=current_user_id,
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found",
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this meal plan",
        )

    return MealPlanResponse(
        id=meal_plan.id,
        owner_id=meal_plan.owner_id,
        year=meal_plan.year,
        week_number=meal_plan.week_number,
        days={
            day_index: DailyPlanResponse(
                lunch_recipe_id=plan.lunch_recipe_id,
                dinner_recipe_id=plan.dinner_recipe_id,
            )
            for day_index, plan in meal_plan.days.items()
        },
    )


@router.get("/meal-plans/", response_model=List[MealPlanResponse])
async def list_meal_plans(
        current_user_id: UUID = Depends(get_current_user_id),
        use_case: ListMealPlansUseCase = Depends(get_list_meal_plans_use_case)
):
    meal_plans = await use_case.execute(owner_id=current_user_id)
    return [
        MealPlanResponse(
            id=mp.id,
            owner_id=mp.owner_id,
            year=mp.year,
            week_number=mp.week_number,
            days={
                day_index: DailyPlanResponse(
                    lunch_recipe_id=plan.lunch_recipe_id,
                    dinner_recipe_id=plan.dinner_recipe_id,
                )
                for day_index, plan in mp.days.items()
            },
        )
        for mp in meal_plans
    ]

