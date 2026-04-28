from pydantic import BaseModel, field_validator, ConfigDict
from uuid import UUID
from typing import Optional


class IngredientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    category: str

    @field_validator('category', mode='before')
    @classmethod
    def serialize_category(cls, v):
        if hasattr(v, 'name'):
            return v.name
        return v


class CreateIngredientRequest(BaseModel):
    name: str
    category: str

    @field_validator('category')
    @classmethod
    def validate_category(cls, v: str) -> str:
        from src.Domain.ValueObject.Category import Category
        valid = {c.name for c in Category}
        if v.upper() not in valid:
            raise ValueError(
                f"Invalid category '{v}'. Valid options: {', '.join(sorted(valid))}"
            )
        return v.upper()


class UpdateIngredientRequest(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None

    @field_validator('category')
    @classmethod
    def validate_category(cls, v: str) -> str:
        if v is None:
            return v
        from src.Domain.ValueObject.Category import Category
        valid = {c.name for c in Category}
        if v.upper() not in valid:
            raise ValueError(
                f"Invalid category '{v}'. Valid options: {', '.join(sorted(valid))}"
            )
        return v.upper()
