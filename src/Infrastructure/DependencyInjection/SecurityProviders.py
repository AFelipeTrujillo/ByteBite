from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.Infrastructure.Security.JwtAuthService import JwtAuthService
from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_auth_service() -> JwtAuthService:
    return JwtAuthService()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    auth_service = get_auth_service()
    user_id = auth_service.get_user_id_from_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return type('User', (), {'id': UUID(user_id)})