from uuid import UUID, uuid4
from typing import List, Dict
from src.Domain.Entity.Recipe import Recipe, RecipeIngredient
from src.Domain.ValueObject.IngredientQuantity import IngredientQuantity
from src.Domain.ValueObject.Unit import Unit
from src.Domain.Repository.RecipeRepository import RecipeRepository


class CreateRecipeUseCase:
    def __init__(self, recipe_repo: RecipeRepository):
        self.recipe_repo = recipe_repo

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
        return recipe
