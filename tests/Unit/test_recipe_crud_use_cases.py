import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.Application.UseCase.CreateRecipeUseCase import CreateRecipeUseCase
from src.Application.UseCase.GetRecipeByIdUseCase import GetRecipeByIdUseCase
from src.Application.UseCase.UpdateRecipeUseCase import UpdateRecipeUseCase
from src.Application.UseCase.DeleteRecipeUseCase import DeleteRecipeUseCase
from src.Domain.Entity.Recipe import Recipe, RecipeIngredient
from src.Domain.ValueObject.IngredientQuantity import IngredientQuantity
from src.Domain.ValueObject.Unit import Unit


@pytest.fixture
def mock_recipe_repo():
    return MagicMock()


@pytest.fixture
def sample_recipe(user_id=None):
    if user_id is None:
        user_id = uuid4()
    return Recipe(
        id=uuid4(),
        owner_id=user_id,
        name="Test Recipe",
        ingredients=[
            RecipeIngredient(
                ingredient_id=uuid4(),
                quantity=IngredientQuantity(amount=200, unit=Unit.GRAMS),
            )
        ],
        references=["https://example.com"],
        invited_users=[],
    )


# --- CREATE ---


@pytest.mark.asyncio
async def test_create_recipe_success(mock_recipe_repo):
    # Arrange
    mock_recipe_repo.save = AsyncMock()
    use_case = CreateRecipeUseCase(mock_recipe_repo)
    owner_id = uuid4()
    ingredient_id = uuid4()

    ingredients_data = [
        {
            "ingredient_id": str(ingredient_id),
            "quantity": {"amount": 500, "unit": "GRAMS"},
        }
    ]

    # Act
    recipe = await use_case.execute(
        owner_id=owner_id,
        name="Pasta Carbonara",
        ingredients=ingredients_data,
        references=["https://recipes.com/carbonara"],
    )

    # Assert
    assert recipe.name == "Pasta Carbonara"
    assert recipe.owner_id == owner_id
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity.amount == 500
    assert recipe.ingredients[0].quantity.unit == Unit.GRAMS
    mock_recipe_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_recipe_without_references(mock_recipe_repo):
    # Arrange
    mock_recipe_repo.save = AsyncMock()
    use_case = CreateRecipeUseCase(mock_recipe_repo)
    ingredient_id = uuid4()

    ingredients_data = [
        {
            "ingredient_id": str(ingredient_id),
            "quantity": {"amount": 1, "unit": "UNITS"},
        }
    ]

    # Act
    recipe = await use_case.execute(
        owner_id=uuid4(),
        name="Simple Egg",
        ingredients=ingredients_data,
    )

    # Assert
    assert recipe.references == []
    mock_recipe_repo.save.assert_called_once()


# --- GET BY ID ---


@pytest.mark.asyncio
async def test_get_recipe_by_id_success(mock_recipe_repo, sample_recipe):
    # Arrange
    mock_recipe_repo.get_by_id = AsyncMock(return_value=sample_recipe)
    use_case = GetRecipeByIdUseCase(mock_recipe_repo)

    # Act
    recipe = await use_case.execute(
        recipe_id=sample_recipe.id,
        user_id=sample_recipe.owner_id,
    )

    # Assert
    assert recipe.id == sample_recipe.id
    assert recipe.name == "Test Recipe"
    mock_recipe_repo.get_by_id.assert_called_once_with(sample_recipe.id)


@pytest.mark.asyncio
async def test_get_recipe_by_id_not_found(mock_recipe_repo):
    # Arrange
    mock_recipe_repo.get_by_id = AsyncMock(return_value=None)
    use_case = GetRecipeByIdUseCase(mock_recipe_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="Recipe not found"):
        await use_case.execute(recipe_id=uuid4(), user_id=uuid4())


@pytest.mark.asyncio
async def test_get_recipe_by_id_forbidden(mock_recipe_repo, sample_recipe):
    # Arrange
    mock_recipe_repo.get_by_id = AsyncMock(return_value=sample_recipe)
    use_case = GetRecipeByIdUseCase(mock_recipe_repo)
    other_user_id = uuid4()

    # Act & Assert
    with pytest.raises(PermissionError, match="do not have access"):
        await use_case.execute(
            recipe_id=sample_recipe.id,
            user_id=other_user_id,
        )


# --- UPDATE ---


@pytest.mark.asyncio
async def test_update_recipe_success(mock_recipe_repo, sample_recipe):
    # Arrange
    mock_recipe_repo.get_by_id = AsyncMock(return_value=sample_recipe)
    mock_recipe_repo.update = AsyncMock()
    use_case = UpdateRecipeUseCase(mock_recipe_repo)

    # Act
    updated = await use_case.execute(
        recipe_id=sample_recipe.id,
        user_id=sample_recipe.owner_id,
        name="Updated Recipe Name",
    )

    # Assert
    assert updated.name == "Updated Recipe Name"
    assert len(updated.ingredients) == 1  # unchanged
    mock_recipe_repo.update.assert_called_once()


@pytest.mark.asyncio
async def test_update_recipe_not_found(mock_recipe_repo):
    # Arrange
    mock_recipe_repo.get_by_id = AsyncMock(return_value=None)
    use_case = UpdateRecipeUseCase(mock_recipe_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="Recipe not found"):
        await use_case.execute(recipe_id=uuid4(), user_id=uuid4())


@pytest.mark.asyncio
async def test_update_recipe_forbidden(mock_recipe_repo, sample_recipe):
    # Arrange
    mock_recipe_repo.get_by_id = AsyncMock(return_value=sample_recipe)
    use_case = UpdateRecipeUseCase(mock_recipe_repo)

    # Act & Assert
    with pytest.raises(PermissionError, match="only update your own"):
        await use_case.execute(
            recipe_id=sample_recipe.id,
            user_id=uuid4(),  # different user
            name="Hacked Recipe",
        )


# --- DELETE ---


@pytest.mark.asyncio
async def test_delete_recipe_success(mock_recipe_repo, sample_recipe):
    # Arrange
    mock_recipe_repo.get_by_id = AsyncMock(return_value=sample_recipe)
    mock_recipe_repo.delete = AsyncMock()
    use_case = DeleteRecipeUseCase(mock_recipe_repo)

    # Act
    await use_case.execute(
        recipe_id=sample_recipe.id,
        user_id=sample_recipe.owner_id,
    )

    # Assert
    mock_recipe_repo.delete.assert_called_once_with(sample_recipe.id)


@pytest.mark.asyncio
async def test_delete_recipe_not_found(mock_recipe_repo):
    # Arrange
    mock_recipe_repo.get_by_id = AsyncMock(return_value=None)
    use_case = DeleteRecipeUseCase(mock_recipe_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="Recipe not found"):
        await use_case.execute(recipe_id=uuid4(), user_id=uuid4())


@pytest.mark.asyncio
async def test_delete_recipe_forbidden(mock_recipe_repo, sample_recipe):
    # Arrange
    mock_recipe_repo.get_by_id = AsyncMock(return_value=sample_recipe)
    use_case = DeleteRecipeUseCase(mock_recipe_repo)

    # Act & Assert
    with pytest.raises(PermissionError, match="only delete your own"):
        await use_case.execute(
            recipe_id=sample_recipe.id,
            user_id=uuid4(),  # different user
        )
