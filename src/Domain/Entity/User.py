from dataclasses import dataclass
from uuid import UUID
from typing import Optional

@dataclass
class User:
    id: UUID
    email: str
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True