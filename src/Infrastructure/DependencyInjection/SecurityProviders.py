from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.Infrastructure.Security.JwtAuthService import JwtAuthService
from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_auth_service() -> JwtAuthService:
    return JwtAuthService()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    auth_service = get_auth_service()
    payload = auth_service.decode_token(token)

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return type('User', (), {
        'id': UUID(user_id),
        'role': payload.get("role", "user")
    })


async def get_current_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user
