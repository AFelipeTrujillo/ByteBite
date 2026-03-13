from fastapi import APIRouter, Depends
from typing import List
from src.Infrastructure.Delivery.Http.Schemas.RecipeSchema import RecipeResponse
from src.Application.UseCase.GetRecipesUseCase import GetRecipesUseCase
from src.Infrastructure.DependencyInjection.MongoProviders import get_get_recipes_use_case
from src.Infrastructure.DependencyInjection.SecurityProviders import get_current_user

router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.get("/", response_model=List[RecipeResponse])
async def get_recipes(
    current_user = Depends(get_current_user),
    use_case: GetRecipesUseCase = Depends(get_get_recipes_use_case)
):
    recipes = await use_case.execute(owner_id=current_user.id)
    return recipes