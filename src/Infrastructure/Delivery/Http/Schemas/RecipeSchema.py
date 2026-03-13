from pydantic import BaseModel, field_validator, ConfigDict
from uuid import UUID
from typing import List

class IngredientQuantitySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    amount: float
    unit: str

    @field_validator('unit', mode='before')
    @classmethod
    def serialize_unit(cls, v):
        if hasattr(v, 'name'):
            return v.name
        return v

class RecipeIngredientSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ingredient_id: UUID
    quantity: IngredientQuantitySchema

class RecipeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_id: UUID
    name: str
    ingredients: List[RecipeIngredientSchema]
    references: List[str]