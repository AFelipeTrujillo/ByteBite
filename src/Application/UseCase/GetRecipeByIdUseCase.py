from uuid import UUID
from src.Domain.Entity.Recipe import Recipe
from src.Domain.Repository.RecipeRepository import RecipeRepository


class GetRecipeByIdUseCase:
    def __init__(self, recipe_repo: RecipeRepository):
        self.recipe_repo = recipe_repo

    async def execute(self, recipe_id: UUID, user_id: UUID) -> Recipe:
        recipe = await self.recipe_repo.get_by_id(recipe_id)

        if not recipe:
            raise ValueError("Recipe not found")

        # Only owner or invited users can view
        if recipe.owner_id != user_id and user_id not in recipe.invited_users:
            raise PermissionError("You do not have access to this recipe")

        return recipe
