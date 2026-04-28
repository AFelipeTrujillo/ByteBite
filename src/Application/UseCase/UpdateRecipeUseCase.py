from uuid import UUID
from typing import List, Dict
from src.Domain.Entity.Recipe import Recipe, RecipeIngredient
from src.Domain.ValueObject.IngredientQuantity import IngredientQuantity
from src.Domain.ValueObject.Unit import Unit
from src.Domain.Repository.RecipeRepository import RecipeRepository


class UpdateRecipeUseCase:
    def __init__(self, recipe_repo: RecipeRepository):
        self.recipe_repo = recipe_repo

    async def execute(
        self,
        recipe_id: UUID,
        user_id: UUID,
        name: str | None = None,
        ingredients: List[Dict] | None = None,
        references: List[str] | None = None,
    ) -> Recipe:
        recipe = await self.recipe_repo.get_by_id(recipe_id)

        if not recipe:
            raise ValueError("Recipe not found")

        if recipe.owner_id != user_id:
            raise PermissionError("You can only update your own recipes")

        if name is not None:
            recipe.name = name

        if ingredients is not None:
            recipe.ingredients = [
                RecipeIngredient(
                    ingredient_id=UUID(item["ingredient_id"]),
                    quantity=IngredientQuantity(
                        amount=item["quantity"]["amount"],
                        unit=Unit[item["quantity"]["unit"]],
                    ),
                )
                for item in ingredients
            ]

        if references is not None:
            recipe.references = references

        await self.recipe_repo.update(recipe)
        return recipe
