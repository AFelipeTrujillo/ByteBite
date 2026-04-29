from uuid import UUID, uuid4
from typing import List, Dict
from src.Domain.Entity.Recipe import Recipe, RecipeIngredient
from src.Domain.ValueObject.IngredientQuantity import IngredientQuantity
from src.Domain.ValueObject.Unit import Unit
from src.Domain.Repository.RecipeRepository import RecipeRepository
from src.Domain.Repository.IngredientRepository import IngredientRepository


class CreateRecipeUseCase:
    def __init__(self, recipe_repo: RecipeRepository, ingredient_repo: IngredientRepository):
        self.recipe_repo = recipe_repo
        self.ingredient_repo = ingredient_repo

    async def execute(
        self,
        owner_id: UUID,
        name: str,
        ingredients: List[Dict],
        references: List[str] | None = None,
    ) -> Recipe:
        recipe_ingredients = []
        for item in ingredients:
            recipe_ingredients.append(
                RecipeIngredient(
                    ingredient_id=UUID(item["ingredient_id"]),
                    quantity=IngredientQuantity(
                        amount=item["quantity"]["amount"],
                        unit=Unit[item["quantity"]["unit"]],
                    ),
                )
            )

        recipe = Recipe(
            id=uuid4(),
            owner_id=owner_id,
            name=name,
            ingredients=recipe_ingredients,
            references=references or [],
        )

        await self.recipe_repo.save(recipe)

        # Resolve ingredient names before returning
        for ing in recipe.ingredients:
            ingredient = await self.ingredient_repo.get_by_id(ing.ingredient_id)
            ing.ingredient_name = ingredient.name if ingredient else "Unknown"

        return recipe
