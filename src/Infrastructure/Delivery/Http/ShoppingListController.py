from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from src.Application.UseCase.GenerateShoppingList import GenerateShoppingList

router = APIRouter()

@router.get("/shopping-list/{meal_plan_id}")
async def generate_list(
    meal_plan_id: UUID,
    use_case: GenerateShoppingList = Depends()
):
    try:
        return await use_case.execute(meal_plan_id=meal_plan_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


