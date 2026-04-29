from typing import List
from uuid import UUID
from src.Domain.Entity.Recipe import Recipe
from src.Domain.Repository.RecipeRepository import RecipeRepository
from src.Domain.Repository.IngredientRepository import IngredientRepository


class GetRecipesUseCase:
    def __init__(self, repository: RecipeRepository, ingredient_repo: IngredientRepository):
        self.repository = repository
        self.ingredient_repo = ingredient_repo

    async def execute(self, owner_id: UUID) -> List[Recipe]:
        recipes = await self.repository.find_by_owner(owner_id)
        await self._resolve_ingredient_names(recipes)
        return recipes

    async def _resolve_ingredient_names(self, recipes: List[Recipe]) -> None:
        for recipe in recipes:
            for ing in recipe.ingredients:
                ingredient = await self.ingredient_repo.get_by_id(ing.ingredient_id)
                ing.ingredient_name = ingredient.name if ingredient else "Unknown"
