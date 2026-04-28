from uuid import uuid4
from src.Domain.Entity.User import User
from src.Domain.Repository.UserRepository import UserRepository
from src.Application.Service.AuthService import AuthService


class RegisterUseCase:
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service

    async def execute(self, email: str, password: str, full_name: str | None = None) -> User:
        # 1. Check if email already exists
        existing_user = await self.user_repository.find_by_email(email)
        if existing_user:
            raise ValueError(f"Email '{email}' is already registered")

        # 2. Hash the password
        hashed_password = self.auth_service.hash_password(password)

        # 3. Create and save the user
        user = User(
            id=uuid4(),
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            is_active=True
        )

        await self.user_repository.save(user)

        return user
