import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.Application.UseCase.RegisterUseCase import RegisterUseCase
from src.Domain.Entity.User import User


@pytest.mark.asyncio
async def test_register_success():
    # Arrange
    email = "newuser@example.com"
    password = "securepass123"
    full_name = "New User"

    mock_repo = MagicMock()
    mock_repo.find_by_email = AsyncMock(return_value=None)  # No existing user
    mock_repo.save = AsyncMock()

    mock_auth = MagicMock()
    mock_auth.hash_password.return_value = "hashed_version"

    use_case = RegisterUseCase(mock_repo, mock_auth)

    # Act
    user = await use_case.execute(
        email=email,
        password=password,
        full_name=full_name,
    )

    # Assert
    assert user.email == email
    assert user.full_name == full_name
    assert user.hashed_password == "hashed_version"
    assert user.is_active is True
    assert user.id is not None

    mock_repo.find_by_email.assert_called_once_with(email)
    mock_auth.hash_password.assert_called_once_with(password)
    mock_repo.save.assert_called_once_with(user)


@pytest.mark.asyncio
async def test_register_duplicate_email():
    # Arrange
    email = "existing@example.com"
    existing_user = User(
        id=uuid4(),
        email=email,
        hashed_password="hashed",
        is_active=True,
    )

    mock_repo = MagicMock()
    mock_repo.find_by_email = AsyncMock(return_value=existing_user)

    mock_auth = MagicMock()

    use_case = RegisterUseCase(mock_repo, mock_auth)

    # Act & Assert
    with pytest.raises(ValueError, match="already registered"):
        await use_case.execute(
            email=email,
            password="anypassword",
            full_name=None,
        )

    mock_repo.find_by_email.assert_called_once_with(email)
    mock_auth.hash_password.assert_not_called()
    mock_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_register_without_full_name():
    # Arrange
    email = "noname@example.com"
    password = "securepass123"

    mock_repo = MagicMock()
    mock_repo.find_by_email = AsyncMock(return_value=None)
    mock_repo.save = AsyncMock()

    mock_auth = MagicMock()
    mock_auth.hash_password.return_value = "hashed_version"

    use_case = RegisterUseCase(mock_repo, mock_auth)

    # Act
    user = await use_case.execute(
        email=email,
        password=password,
        full_name=None,
    )

    # Assert
    assert user.email == email
    assert user.full_name is None
    assert user.is_active is True

    mock_repo.save.assert_called_once()
