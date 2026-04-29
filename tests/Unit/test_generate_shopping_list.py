import pytest
from uuid import uuid4
from unittest.mock import AsyncMock

from src.Domain.Entity.MealPlan import MealPlan, DailyPlan
from src.Domain.Entity.Recipe import Recipe, RecipeIngredient
from src.Domain.Entity.Ingredient import Ingredient
from src.Domain.ValueObject.IngredientQuantity import IngredientQuantity
from src.Domain.ValueObject.Unit import Unit
from src.Domain.ValueObject.Category import Category
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

    flour_ingredient = Ingredient(
        id=flour_id,
        name="Flour",
        category=Category.PANTRY,
    )
    mock_ingredient_repo = AsyncMock()
    mock_ingredient_repo.get_by_id.return_value = flour_ingredient

    use_case = GenerateShoppingList(
        mock_meal_plan_repo,
        mock_recipe_repo,
        mock_ingredient_repo
    )

    grouped_list = await use_case.execute(meal_plan.id, user_id)

    # Assert grouped response structure
    assert grouped_list.meal_plan_id == meal_plan.id
    assert len(grouped_list.categories) == 1
    assert grouped_list.categories[0].category == "Pantry Essentials"
    assert len(grouped_list.categories[0].items) == 1

    item = grouped_list.categories[0].items[0]
    assert item.ingredient_name == "Flour"
    assert item.amount == 500
    assert item.unit == Unit.GRAMS
    assert item.category == Category.PANTRY
    assert item.checked is False


@pytest.mark.asyncio
async def test_generate_shopping_list_not_found():
    # Arrange
    user_id = uuid4()
    meal_plan_id = uuid4()

    mock_meal_plan_repo = AsyncMock()
    mock_meal_plan_repo.get_by_id.return_value = None

    mock_recipe_repo = AsyncMock()
    mock_ingredient_repo = AsyncMock()

    use_case = GenerateShoppingList(
        mock_meal_plan_repo,
        mock_recipe_repo,
        mock_ingredient_repo
    )

    # Act & Assert
    with pytest.raises(ValueError, match="Meal Plan not found"):
        await use_case.execute(meal_plan_id, user_id)


@pytest.mark.asyncio
async def test_generate_shopping_list_forbidden():
    # Arrange
    owner_id = uuid4()
    other_user_id = uuid4()

    meal_plan = MealPlan(
        id=uuid4(),
        owner_id=owner_id,
        year=2026,
        week_number=10,
        days={},
    )

    mock_meal_plan_repo = AsyncMock()
    mock_meal_plan_repo.get_by_id.return_value = meal_plan

    mock_recipe_repo = AsyncMock()
    mock_ingredient_repo = AsyncMock()

    use_case = GenerateShoppingList(
        mock_meal_plan_repo,
        mock_recipe_repo,
        mock_ingredient_repo
    )

    # Act & Assert
    with pytest.raises(PermissionError, match="do not have access"):
        await use_case.execute(meal_plan.id, other_user_id)
