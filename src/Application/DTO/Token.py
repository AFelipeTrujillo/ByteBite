from dataclasses import dataclass

@dataclass(frozen=True)
class TokenDTO:
    access_token: str
    token_type: str = "bearer"