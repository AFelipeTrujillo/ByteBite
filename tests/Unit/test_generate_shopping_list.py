import pytest
from uuid import uuid4
from unittest.mock import AsyncMock

from src.Domain.Entity.MealPlan import MealPlan, DailyPlan
from src.Domain.Entity.Recipe import Recipe, RecipeIngredient
from src.Domain.ValueObject.IngredientQuantity import IngredientQuantity
from src.Domain.ValueObject.Unit import Unit
from src.Application.UseCase.GenerateShoppingList import GenerateShoppingList

@pytest.mark.asyncio
async def test_should_consolidate_ingredients_from_multiple_recipes():
    user_id = uuid4()
    flour_id = uuid4()

    recipe1 = Recipe(
        id          =uuid4(),
        owner_id    =user_id,
        name        ="Cookies",
        ingredients = [
            RecipeIngredient( flour_id, IngredientQuantity(300, Unit.GRAMS))
        ]
    )

    recipe2 = Recipe(
        id          = uuid4(),
        owner_id    = user_id,
        name        = "Bread",
        ingredients = [
            RecipeIngredient (flour_id, IngredientQuantity(200, Unit.GRAMS))
        ]
    )

    meal_plan = MealPlan(
        id          = uuid4(),
        owner_id    = user_id,
        year        = 2026,
        week_number = 10,
        days        = {
            0: DailyPlan(lunch_recipe_id=recipe1.id, dinner_recipe_id=recipe2.id)
        }
    )

    mock_meal_plan_repo = AsyncMock()
    mock_meal_plan_repo.get_by_id.return_value = meal_plan

    mock_recipe_repo = AsyncMock()
    mock_recipe_repo.get_by_ids.return_value = [recipe1, recipe2]

    mock_ingredient_repo = AsyncMock()
    mock_ingredient_repo.get_name_by_id.return_value = "Flour"

    use_case = GenerateShoppingList(
        mock_meal_plan_repo,
        mock_recipe_repo,
        mock_ingredient_repo
    )

    shopping_list = await use_case.execute(meal_plan.id)

    assert len(shopping_list) == 1
    assert shopping_list[0].ingredient_name == "Flour"
    assert shopping_list[0].amount == 500
    assert shopping_list[0].unit == Unit.GRAMS

    
