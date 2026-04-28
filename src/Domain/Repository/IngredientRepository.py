from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, List

from src.Domain.Entity.Ingredient import Ingredient


class IngredientRepository(ABC):

    @abstractmethod
    async def get_name_by_id(self, ingredient_id: UUID) -> str:
        pass

    @abstractmethod
    async def get_by_id(self, ingredient_id: UUID) -> Optional[Ingredient]:
        pass

    @abstractmethod
    async def list_all(self) -> List[Ingredient]:
        pass

    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[Ingredient]:
        pass

    @abstractmethod
    async def save(self, ingredient: Ingredient) -> None:
        pass

    @abstractmethod
    async def update(self, ingredient: Ingredient) -> None:
        pass

    @abstractmethod
    async def delete(self, ingredient_id: UUID) -> None:
        pass
