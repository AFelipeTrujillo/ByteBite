from fastapi import APIRouter, Depends
from typing import List
from uuid import  UUID

from src.Infrastructure.Delivery.Http.Schemas.ShoppingListSchema import ShoppingListItemResponse
from src.Infrastructure.DependencyInjection.MongoProviders import get_generate_shopping_list_use_case
from src.Application.UseCase.GenerateShoppingList import GenerateShoppingList

router = APIRouter()

@router.get("/shopping-list/{meal_plan_id}", response_model=List[ShoppingListItemResponse])
async def generate_list(
        meal_plan_id: UUID,
        use_case: GenerateShoppingList = Depends(get_generate_shopping_list_use_case)
):

    items_dto = await use_case.execute(meal_plan_id)

    return items_dto
