from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from src.Infrastructure.Delivery.Http.Schemas.IngredientSchema import (
    IngredientResponse,
    CreateIngredientRequest,
    UpdateIngredientRequest,
)
from src.Application.UseCase.ListIngredientsUseCase import ListIngredientsUseCase
from src.Application.UseCase.GetIngredientByIdUseCase import GetIngredientByIdUseCase
from src.Application.UseCase.CreateIngredientUseCase import CreateIngredientUseCase
from src.Application.UseCase.UpdateIngredientUseCase import UpdateIngredientUseCase
from src.Application.UseCase.DeleteIngredientUseCase import DeleteIngredientUseCase
from src.Infrastructure.DependencyInjection.MongoProviders import (
    get_list_ingredients_use_case,
    get_ingredient_by_id_use_case,
    get_create_ingredient_use_case,
    get_update_ingredient_use_case,
    get_delete_ingredient_use_case,
)
from src.Infrastructure.DependencyInjection.SecurityProviders import (
    get_current_user,
    get_current_admin,
)

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])


@router.get("/", response_model=List[IngredientResponse])
async def list_ingredients(
    current_user=Depends(get_current_user),
    use_case: ListIngredientsUseCase = Depends(get_list_ingredients_use_case),
):
    return await use_case.execute()


@router.get("/{ingredient_id}", response_model=IngredientResponse)
async def get_ingredient(
    ingredient_id: UUID,
    current_user=Depends(get_current_user),
    use_case: GetIngredientByIdUseCase = Depends(get_ingredient_by_id_use_case),
):
    try:
        return await use_case.execute(ingredient_id=ingredient_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post(
    "/",
    response_model=IngredientResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_ingredient(
    request: CreateIngredientRequest,
    admin=Depends(get_current_admin),
    use_case: CreateIngredientUseCase = Depends(get_create_ingredient_use_case),
):
    try:
        return await use_case.execute(
            name=request.name,
            category=request.category,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.put("/{ingredient_id}", response_model=IngredientResponse)
async def update_ingredient(
    ingredient_id: UUID,
    request: UpdateIngredientRequest,
    admin=Depends(get_current_admin),
    use_case: UpdateIngredientUseCase = Depends(get_update_ingredient_use_case),
):
    try:
        return await use_case.execute(
            ingredient_id=ingredient_id,
            name=request.name,
            category=request.category,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ingredient(
    ingredient_id: UUID,
    admin=Depends(get_current_admin),
    use_case: DeleteIngredientUseCase = Depends(get_delete_ingredient_use_case),
):
    try:
        await use_case.execute(ingredient_id=ingredient_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
