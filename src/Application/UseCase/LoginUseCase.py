from typing import Optional
from src.Domain.Repository.UserRepository import UserRepository
from src.Application.Service.AuthService import AuthService
from src.Application.DTO.Token import TokenDTO

class LoginUseCase:
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service

    async def execute(self, email: str, password: str) -> TokenDTO:
        # 1. Find user by email
        user = await self.user_repository.find_by_email(email)

        if not user or not user.is_active:
            raise ValueError("Invalid credentials or inactive account")

        # 2. Verify password
        is_valid = self.auth_service.verify_password(password, user.hashed_password)

        if not is_valid:
            raise ValueError("Invalid credentials")

        # 3. Create Access Token (using user ID and email as payload)
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value
        }

        token_string = self.auth_service.create_access_token(token_data)

        return TokenDTO(access_token=token_string)