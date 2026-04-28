import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.Application.UseCase.CreateIngredientUseCase import CreateIngredientUseCase
from src.Application.UseCase.GetIngredientByIdUseCase import GetIngredientByIdUseCase
from src.Application.UseCase.ListIngredientsUseCase import ListIngredientsUseCase
from src.Application.UseCase.UpdateIngredientUseCase import UpdateIngredientUseCase
from src.Application.UseCase.DeleteIngredientUseCase import DeleteIngredientUseCase
from src.Domain.Entity.Ingredient import Ingredient
from src.Domain.ValueObject.Category import Category


@pytest.fixture
def mock_ingredient_repo():
    return MagicMock()


@pytest.fixture
def sample_ingredient():
    return Ingredient(
        id=uuid4(),
        name="Tomato",
        category=Category.VEGETABLES,
    )


# --- LIST ---


@pytest.mark.asyncio
async def test_list_ingredients(mock_ingredient_repo, sample_ingredient):
    # Arrange
    mock_ingredient_repo.list_all = AsyncMock(return_value=[sample_ingredient])
    use_case = ListIngredientsUseCase(mock_ingredient_repo)

    # Act
    ingredients = await use_case.execute()

    # Assert
    assert len(ingredients) == 1
    assert ingredients[0].name == "Tomato"
    mock_ingredient_repo.list_all.assert_called_once()


# --- CREATE ---


@pytest.mark.asyncio
async def test_create_ingredient_success(mock_ingredient_repo):
    # Arrange
    mock_ingredient_repo.find_by_name = AsyncMock(return_value=None)
    mock_ingredient_repo.save = AsyncMock()
    use_case = CreateIngredientUseCase(mock_ingredient_repo)

    # Act
    ingredient = await use_case.execute(name="Garlic", category="VEGETABLES")

    # Assert
    assert ingredient.name == "Garlic"
    assert ingredient.category == Category.VEGETABLES
    mock_ingredient_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_ingredient_duplicate(mock_ingredient_repo, sample_ingredient):
    # Arrange
    mock_ingredient_repo.find_by_name = AsyncMock(return_value=sample_ingredient)
    use_case = CreateIngredientUseCase(mock_ingredient_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="already exists"):
        await use_case.execute(name="Tomato", category="VEGETABLES")

    mock_ingredient_repo.save.assert_not_called()


# --- GET BY ID ---


@pytest.mark.asyncio
async def test_get_ingredient_by_id_success(mock_ingredient_repo, sample_ingredient):
    # Arrange
    mock_ingredient_repo.get_by_id = AsyncMock(return_value=sample_ingredient)
    use_case = GetIngredientByIdUseCase(mock_ingredient_repo)

    # Act
    ingredient = await use_case.execute(ingredient_id=sample_ingredient.id)

    # Assert
    assert ingredient.id == sample_ingredient.id
    assert ingredient.name == "Tomato"


@pytest.mark.asyncio
async def test_get_ingredient_by_id_not_found(mock_ingredient_repo):
    # Arrange
    mock_ingredient_repo.get_by_id = AsyncMock(return_value=None)
    use_case = GetIngredientByIdUseCase(mock_ingredient_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="Ingredient not found"):
        await use_case.execute(ingredient_id=uuid4())


# --- UPDATE ---


@pytest.mark.asyncio
async def test_update_ingredient_name(mock_ingredient_repo, sample_ingredient):
    # Arrange
    mock_ingredient_repo.get_by_id = AsyncMock(return_value=sample_ingredient)
    mock_ingredient_repo.find_by_name = AsyncMock(return_value=None)
    mock_ingredient_repo.update = AsyncMock()
    use_case = UpdateIngredientUseCase(mock_ingredient_repo)

    # Act
    updated = await use_case.execute(
        ingredient_id=sample_ingredient.id,
        name="Roma Tomato",
    )

    # Assert
    assert updated.name == "Roma Tomato"
    assert updated.category == Category.VEGETABLES  # unchanged
    mock_ingredient_repo.update.assert_called_once()


@pytest.mark.asyncio
async def test_update_ingredient_category(mock_ingredient_repo, sample_ingredient):
    # Arrange
    mock_ingredient_repo.get_by_id = AsyncMock(return_value=sample_ingredient)
    mock_ingredient_repo.update = AsyncMock()
    use_case = UpdateIngredientUseCase(mock_ingredient_repo)

    # Act
    updated = await use_case.execute(
        ingredient_id=sample_ingredient.id,
        category="FRUITS",
    )

    # Assert
    assert updated.name == "Tomato"  # unchanged
    assert updated.category == Category.FRUITS
    mock_ingredient_repo.update.assert_called_once()


@pytest.mark.asyncio
async def test_update_ingredient_not_found(mock_ingredient_repo):
    # Arrange
    mock_ingredient_repo.get_by_id = AsyncMock(return_value=None)
    use_case = UpdateIngredientUseCase(mock_ingredient_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="Ingredient not found"):
        await use_case.execute(ingredient_id=uuid4(), name="New Name")


# --- DELETE ---


@pytest.mark.asyncio
async def test_delete_ingredient_success(mock_ingredient_repo, sample_ingredient):
    # Arrange
    mock_ingredient_repo.get_by_id = AsyncMock(return_value=sample_ingredient)
    mock_ingredient_repo.delete = AsyncMock()
    use_case = DeleteIngredientUseCase(mock_ingredient_repo)

    # Act
    await use_case.execute(ingredient_id=sample_ingredient.id)

    # Assert
    mock_ingredient_repo.delete.assert_called_once_with(sample_ingredient.id)


@pytest.mark.asyncio
async def test_delete_ingredient_not_found(mock_ingredient_repo):
    # Arrange
    mock_ingredient_repo.get_by_id = AsyncMock(return_value=None)
    use_case = DeleteIngredientUseCase(mock_ingredient_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="Ingredient not found"):
        await use_case.execute(ingredient_id=uuid4())
