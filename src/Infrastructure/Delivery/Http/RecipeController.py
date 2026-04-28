from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from src.Infrastructure.Delivery.Http.Schemas.RecipeSchema import (
    RecipeResponse,
    CreateRecipeRequest,
    UpdateRecipeRequest,
)
from src.Application.UseCase.GetRecipesUseCase import GetRecipesUseCase
from src.Application.UseCase.GetRecipeByIdUseCase import GetRecipeByIdUseCase
from src.Application.UseCase.CreateRecipeUseCase import CreateRecipeUseCase
from src.Application.UseCase.UpdateRecipeUseCase import UpdateRecipeUseCase
from src.Application.UseCase.DeleteRecipeUseCase import DeleteRecipeUseCase
from src.Infrastructure.DependencyInjection.MongoProviders import (
    get_get_recipes_use_case,
    get_get_recipe_by_id_use_case,
    get_create_recipe_use_case,
    get_update_recipe_use_case,
    get_delete_recipe_use_case,
)
from src.Infrastructure.DependencyInjection.SecurityProviders import get_current_user

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.get("/", response_model=List[RecipeResponse])
async def get_recipes(
    current_user=Depends(get_current_user),
    use_case: GetRecipesUseCase = Depends(get_get_recipes_use_case),
):
    recipes = await use_case.execute(owner_id=current_user.id)
    return recipes


@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(
    recipe_id: UUID,
    current_user=Depends(get_current_user),
    use_case: GetRecipeByIdUseCase = Depends(get_get_recipe_by_id_use_case),
):
    try:
        recipe = await use_case.execute(recipe_id=recipe_id, user_id=current_user.id)
        return recipe
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.post("/", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    request: CreateRecipeRequest,
    current_user=Depends(get_current_user),
    use_case: CreateRecipeUseCase = Depends(get_create_recipe_use_case),
):
    try:
        recipe = await use_case.execute(
            owner_id=current_user.id,
            name=request.name,
            ingredients=[item.model_dump() for item in request.ingredients],
            references=request.references,
        )
        return recipe
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid unit: {e}",
        )


@router.put("/{recipe_id}", response_model=RecipeResponse)
async def update_recipe(
    recipe_id: UUID,
    request: UpdateRecipeRequest,
    current_user=Depends(get_current_user),
    use_case: UpdateRecipeUseCase = Depends(get_update_recipe_use_case),
):
    try:
        ingredients_data = (
            [item.model_dump() for item in request.ingredients]
            if request.ingredients is not None
            else None
        )
        recipe = await use_case.execute(
            recipe_id=recipe_id,
            user_id=current_user.id,
            name=request.name,
            ingredients=ingredients_data,
            references=request.references,
        )
        return recipe
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid unit: {e}",
        )


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
    recipe_id: UUID,
    current_user=Depends(get_current_user),
    use_case: DeleteRecipeUseCase = Depends(get_delete_recipe_use_case),
):
    try:
        await use_case.execute(recipe_id=recipe_id, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
