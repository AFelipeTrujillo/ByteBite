import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.Application.UseCase.GetMealPlanByIdUseCase import GetMealPlanByIdUseCase
from src.Domain.Entity.MealPlan import MealPlan, DailyPlan


@pytest.fixture
def mock_meal_plan_repo():
    return MagicMock()


@pytest.fixture
def sample_meal_plan():
    owner_id = uuid4()
    recipe_id = uuid4()
    return MealPlan(
        id=uuid4(),
        owner_id=owner_id,
        year=2026,
        week_number=11,
        days={
            1: DailyPlan(lunch_recipe_id=recipe_id, dinner_recipe_id=None),
            2: DailyPlan(lunch_recipe_id=None, dinner_recipe_id=recipe_id),
        },
    )


@pytest.mark.asyncio
async def test_get_meal_plan_by_id_success(mock_meal_plan_repo, sample_meal_plan):
    # Arrange
    mock_meal_plan_repo.get_by_id = AsyncMock(return_value=sample_meal_plan)
    use_case = GetMealPlanByIdUseCase(mock_meal_plan_repo)

    # Act
    result = await use_case.execute(
        meal_plan_id=sample_meal_plan.id,
        user_id=sample_meal_plan.owner_id,
    )

    # Assert
    assert result.id == sample_meal_plan.id
    assert result.owner_id == sample_meal_plan.owner_id
    assert result.year == 2026
    assert result.week_number == 11
    assert len(result.days) == 2
    mock_meal_plan_repo.get_by_id.assert_called_once_with(sample_meal_plan.id)


@pytest.mark.asyncio
async def test_get_meal_plan_by_id_not_found(mock_meal_plan_repo):
    # Arrange
    mock_meal_plan_repo.get_by_id = AsyncMock(return_value=None)
    use_case = GetMealPlanByIdUseCase(mock_meal_plan_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="Meal plan not found"):
        await use_case.execute(meal_plan_id=uuid4(), user_id=uuid4())


@pytest.mark.asyncio
async def test_get_meal_plan_by_id_forbidden(mock_meal_plan_repo, sample_meal_plan):
    # Arrange
    mock_meal_plan_repo.get_by_id = AsyncMock(return_value=sample_meal_plan)
    use_case = GetMealPlanByIdUseCase(mock_meal_plan_repo)
    other_user_id = uuid4()

    # Act & Assert
    with pytest.raises(PermissionError, match="do not have access"):
        await use_case.execute(
            meal_plan_id=sample_meal_plan.id,
            user_id=other_user_id,
        )
