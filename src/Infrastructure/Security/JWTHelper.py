import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
from uuid import UUID
from src.Infrastructure.Configs.Settings import settings


class JWTHelper:
    _ALGORITHM = "HS256"

    @staticmethod
    def create_access_token(user_id: UUID, expires_delta: Optional[timedelta] = None) -> str:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {
            "sub": str(user_id),
            "exp": expire,
            "iat": datetime.now(timezone.utc)
        }

        return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=JWTHelper._ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> Dict:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[JWTHelper._ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.PyJWTError:
            raise ValueError("Invalid token")