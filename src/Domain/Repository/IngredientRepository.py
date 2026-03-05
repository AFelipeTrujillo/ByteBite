from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

from src.Domain.Entity.Ingredient import Ingredient


class IngredientRepository(ABC):

    @abstractmethod
    async def get_name_by_id(self, ingredient_id: UUID) -> str:
        pass

    @abstractmethod
    async def get_by_id(self, ingredient_id: UUID) -> Optional[Ingredient]:
        pass