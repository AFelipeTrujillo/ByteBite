from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from src.Application.UseCase.GenerateShoppingList import GenerateShoppingList
from src.Infrastructure.Persistence.MongoClient import MongoClient
from src.Infrastructure.Persistence.MongoRecipeRepository import MongoRecipeRepository

router = APIRouter()

def get_generate_shopping_list_use_case():
    client = MongoClient()
    recipe_repo = MongoRecipeRepository(client.get_collection("recipes"))
    meal_plan_repo = ...
    ingredient_repo = ...

@router.get("/shopping-list/{meal_plan_id}")
async def generate_list(
    meal_plan_id: UUID,
    use_case: GenerateShoppingList = Depends(get_generate_shopping_list_use_case)
):
    try:
        return await use_case.execute(meal_plan_id=meal_plan_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


