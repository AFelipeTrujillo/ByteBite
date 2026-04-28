from uuid import UUID
from src.Domain.Repository.RecipeRepository import RecipeRepository


class DeleteRecipeUseCase:
    def __init__(self, recipe_repo: RecipeRepository):
        self.recipe_repo = recipe_repo

    async def execute(self, recipe_id: UUID, user_id: UUID) -> None:
        recipe = await self.recipe_repo.get_by_id(recipe_id)

        if not recipe:
            raise ValueError("Recipe not found")

        if recipe.owner_id != user_id:
            raise PermissionError("You can only delete your own recipes")

        await self.recipe_repo.delete(recipe_id)
