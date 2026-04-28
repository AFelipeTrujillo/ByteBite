from uuid import UUID
from src.Domain.Entity.Ingredient import Ingredient
from src.Domain.Repository.IngredientRepository import IngredientRepository
from src.Domain.ValueObject.Category import Category


class UpdateIngredientUseCase:
    def __init__(self, ingredient_repo: IngredientRepository):
        self.ingredient_repo = ingredient_repo

    async def execute(
        self,
        ingredient_id: UUID,
        name: str | None = None,
        category: str | None = None,
    ) -> Ingredient:
        ingredient = await self.ingredient_repo.get_by_id(ingredient_id)

        if not ingredient:
            raise ValueError("Ingredient not found")

        if name is not None:
            # Check if new name conflicts with existing ingredient
            existing = await self.ingredient_repo.find_by_name(name)
            if existing and existing.id != ingredient_id:
                raise ValueError(f"Ingredient '{name}' already exists")
            ingredient.name = name.strip()

        if category is not None:
            ingredient.category = Category[category.upper()]

        await self.ingredient_repo.update(ingredient)
        return ingredient
