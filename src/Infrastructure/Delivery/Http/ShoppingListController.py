from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from src.Infrastructure.Delivery.Http.Schemas.ShoppingListSchema import ShoppingListGroupedResponse, ShoppingListItemResponse, CategoryGroupResponse
from src.Infrastructure.DependencyInjection.MongoProviders import get_generate_shopping_list_use_case
from src.Infrastructure.Security.AuthService import get_current_user_id
from src.Application.UseCase.GenerateShoppingList import GenerateShoppingList

router = APIRouter()


@router.get("/shopping-list/{meal_plan_id}", response_model=ShoppingListGroupedResponse)
async def generate_list(
        meal_plan_id: UUID,
        current_user_id: UUID = Depends(get_current_user_id),
        use_case: GenerateShoppingList = Depends(get_generate_shopping_list_use_case)
):
    try:
        grouped_dto = await use_case.execute(
            meal_plan_id=meal_plan_id,
            user_id=current_user_id,
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal Plan not found",
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this meal plan",
        )

    return ShoppingListGroupedResponse(
        meal_plan_id=grouped_dto.meal_plan_id,
        categories=[
            CategoryGroupResponse(
                category=cat.category,
                items=[
                    ShoppingListItemResponse(
                        ingredient_id=item.ingredient_id,
                        ingredient_name=item.ingredient_name,
                        amount=item.amount,
                        unit=item.unit.value,
                        category=item.category.label,
                        checked=item.checked,
                    )
                    for item in cat.items
                ],
            )
            for cat in grouped_dto.categories
        ],
    )

