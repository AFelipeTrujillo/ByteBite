from dataclasses import dataclass
from uuid import UUID
from typing import Optional
from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"


@dataclass
class User:
    id: UUID
    email: str
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.USER
