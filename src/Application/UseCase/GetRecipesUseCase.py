from typing import List
from src.Domain.Entity.Recipe import Recipe
from src.Domain.Repository.RecipeRepository import RecipeRepository

class GetRecipesUseCase:
    def __init__(self, repository: RecipeRepository):
        self.repository = repository

    async def execute(self, owner_id: str) -> List[Recipe]:
         recipes = await self.repository.find_by_owner(owner_id)
         return recipes