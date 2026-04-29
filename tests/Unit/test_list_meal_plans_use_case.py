import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.Application.UseCase.ListMealPlansUseCase import ListMealPlansUseCase
from src.Domain.Entity.MealPlan import MealPlan, DailyPlan


@pytest.fixture
def mock_meal_plan_repo():
    return MagicMock()


@pytest.fixture
def sample_meal_plans(owner_id=None):
    if owner_id is None:
        owner_id = uuid4()
    recipe_id = uuid4()

    meal_plan_1 = MealPlan(
        id=uuid4(),
        owner_id=owner_id,
        year=2026,
        week_number=11,
        days={
            1: DailyPlan(lunch_recipe_id=recipe_id, dinner_recipe_id=None),
            2: DailyPlan(lunch_recipe_id=None, dinner_recipe_id=recipe_id),
        },
    )

    meal_plan_2 = MealPlan(
        id=uuid4(),
        owner_id=owner_id,
        year=2026,
        week_number=10,
        days={
            3: DailyPlan(lunch_recipe_id=recipe_id, dinner_recipe_id=recipe_id),
        },
    )

    return [meal_plan_1, meal_plan_2]


@pytest.mark.asyncio
async def test_list_meal_plans_success(mock_meal_plan_repo, sample_meal_plans):
    # Arrange
    mock_meal_plan_repo.find_by_owner = AsyncMock(return_value=sample_meal_plans)
    use_case = ListMealPlansUseCase(mock_meal_plan_repo)
    owner_id = sample_meal_plans[0].owner_id

    # Act
    result = await use_case.execute(owner_id=owner_id)

    # Assert
    assert len(result) == 2
    assert result[0].id == sample_meal_plans[0].id
    assert result[1].id == sample_meal_plans[1].id
    assert result[0].year == 2026
    assert result[0].week_number == 11
    assert result[1].week_number == 10
    mock_meal_plan_repo.find_by_owner.assert_called_once_with(owner_id)


@pytest.mark.asyncio
async def test_list_meal_plans_empty(mock_meal_plan_repo):
    # Arrange
    mock_meal_plan_repo.find_by_owner = AsyncMock(return_value=[])
    use_case = ListMealPlansUseCase(mock_meal_plan_repo)
    owner_id = uuid4()

    # Act
    result = await use_case.execute(owner_id=owner_id)

    # Assert
    assert result == []
    mock_meal_plan_repo.find_by_owner.assert_called_once_with(owner_id)


@pytest.mark.asyncio
async def test_list_meal_plans_returns_correct_owner(mock_meal_plan_repo, sample_meal_plans):
    # Arrange
    owner_id = uuid4()
    # Return plans for a different owner
    other_owner_id = uuid4()
    other_plans = [
        MealPlan(
            id=uuid4(),
            owner_id=other_owner_id,
            year=2026,
            week_number=11,
            days={},
        )
    ]
    mock_meal_plan_repo.find_by_owner = AsyncMock(return_value=other_plans)
    use_case = ListMealPlansUseCase(mock_meal_plan_repo)

    # Act
    result = await use_case.execute(owner_id=owner_id)

    # Assert
    assert len(result) == 1
    assert result[0].owner_id == other_owner_id  # The repo returns what we ask
    mock_meal_plan_repo.find_by_owner.assert_called_once_with(owner_id)
