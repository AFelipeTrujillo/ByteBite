from typing import List
from src.Domain.Entity.Ingredient import Ingredient
from src.Domain.Repository.IngredientRepository import IngredientRepository


class ListIngredientsUseCase:
    def __init__(self, ingredient_repo: IngredientRepository):
        self.ingredient_repo = ingredient_repo

    async def execute(self) -> List[Ingredient]:
        return await self.ingredient_repo.list_all()
