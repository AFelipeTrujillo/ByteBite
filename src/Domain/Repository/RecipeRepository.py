from abc import ABC, abstractclassmethod, abstractmethod
from typing import List
from uuid import UUID

from src.Domain.Entity.Recipe import Recipe


class RecipeRepository(ABC):

    @abstractmethod
    async def get_by_ids(self, ids: List[UUID]) -> List[Recipe]:
        pass

    @abstractmethod
    async def find_by_owner(self, owner_id: UUID) -> List[Recipe]:
        pass
