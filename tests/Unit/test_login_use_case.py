import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.Application.DTO.Token import TokenDTO
from src.Application.UseCase.LoginUseCase import LoginUseCase
from src.Domain.Entity.User import User


@pytest.mark.asyncio
async def test_login_success():
    # Arrange
    user_id = uuid4()
    email = "test@example.com"
    password = "secure_password"
    hashed_password = "hashed_version"

    # Mocking User
    mock_user = User(
        id=user_id,
        email=email,
        hashed_password=hashed_password,
        is_active=True
    )

    # Mocking Dependencies
    mock_repo = MagicMock()
    mock_repo.find_by_email = AsyncMock(return_value=mock_user)

    mock_auth = MagicMock()
    mock_auth.verify_password.return_value = True
    mock_auth.create_access_token.return_value = "fake_jwt_token"

    use_case = LoginUseCase(mock_repo, mock_auth)

    # Act
    token = await use_case.execute(email, password)

    # Assert
    expected_token = TokenDTO(access_token="fake_jwt_token", token_type="bearer")
    assert token == expected_token
    mock_repo.find_by_email.assert_called_once_with(email)
    mock_auth.verify_password.assert_called_once_with(password, hashed_password)
    mock_auth.create_access_token.assert_called_once()


@pytest.mark.asyncio
async def test_login_invalid_password():
    # Arrange
    mock_user = User(id=uuid4(), email="test@example.com", hashed_password="hashed", is_active=True)
    mock_repo = MagicMock()
    mock_repo.find_by_email = AsyncMock(return_value=mock_user)

    mock_auth = MagicMock()
    mock_auth.verify_password.return_value = False  # Wrong password

    use_case = LoginUseCase(mock_repo, mock_auth)

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid credentials"):
        await use_case.execute("test@example.com", "wrong_password")