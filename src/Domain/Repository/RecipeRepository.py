from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.Domain.Entity.Recipe import Recipe


class RecipeRepository(ABC):

    @abstractmethod
    async def get_by_ids(self, ids: List[UUID]) -> List[Recipe]:
        pass

    @abstractmethod
    async def find_by_owner(self, owner_id: UUID) -> List[Recipe]:
        pass

    @abstractmethod
    async def get_by_id(self, recipe_id: UUID) -> Optional[Recipe]:
        pass

    @abstractmethod
    async def save(self, recipe: Recipe) -> None:
        pass

    @abstractmethod
    async def update(self, recipe: Recipe) -> None:
        pass

    @abstractmethod
    async def delete(self, recipe_id: UUID) -> None:
        pass
