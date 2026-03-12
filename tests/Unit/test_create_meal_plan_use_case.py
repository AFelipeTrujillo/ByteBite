import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from src.Application.UseCase.CreateMealPlan import CreateMealPlan
from src.Infrastructure.Delivery.Http.Schemas.MealPlanSchema import DailyPlanRequest


@pytest.mark.asyncio
async def test_create_meal_plan_success():
    # Arrange
    mock_repo = AsyncMock()
    use_case = CreateMealPlan(meal_plan_repo=mock_repo)

    owner_id = uuid4()
    recipe_id = uuid4()
    days_data = {
        1: DailyPlanRequest(lunch_recipe_id=recipe_id, dinner_recipe_id=None)
    }

    # Act
    result_id = await use_case.execute(
        owner_id=owner_id,
        year=2026,
        week_number=11,
        days_data=days_data
    )

    # Assert
    assert result_id is not None
    # Verify the repo was called once
    mock_repo.save.assert_called_once()

    # Extract the object passed to save() to verify its content
    saved_plan = mock_repo.save.call_args[0][0]
    assert saved_plan.owner_id == owner_id
    assert saved_plan.days[1].lunch_recipe_id == recipe_id