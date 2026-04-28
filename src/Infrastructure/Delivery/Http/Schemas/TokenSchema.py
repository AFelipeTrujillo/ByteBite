from pydantic import BaseModel, ConfigDict, field_validator


class TokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str | None = None

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if '@' not in v or '.' not in v.split('@')[-1]:
            raise ValueError('Invalid email format')
        return v.lower().strip()

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v


class RegisterResponse(BaseModel):
    id: str
    email: str
    full_name: str | None = None
    message: str = "User registered successfully"
