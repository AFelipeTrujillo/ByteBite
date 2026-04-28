from uuid import uuid4
from src.Domain.Entity.Ingredient import Ingredient
from src.Domain.Repository.IngredientRepository import IngredientRepository
from src.Domain.ValueObject.Category import Category


class CreateIngredientUseCase:
    def __init__(self, ingredient_repo: IngredientRepository):
        self.ingredient_repo = ingredient_repo

    async def execute(self, name: str, category: str) -> Ingredient:
        # Check if ingredient name already exists (case-insensitive)
        existing = await self.ingredient_repo.find_by_name(name)
        if existing:
            raise ValueError(f"Ingredient '{name}' already exists")

        ingredient = Ingredient(
            id=uuid4(),
            name=name.strip(),
            category=Category[category.upper()],
        )

        await self.ingredient_repo.save(ingredient)
        return ingredient
