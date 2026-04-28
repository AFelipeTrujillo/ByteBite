from uuid import UUID
from src.Domain.Repository.IngredientRepository import IngredientRepository


class DeleteIngredientUseCase:
    def __init__(self, ingredient_repo: IngredientRepository):
        self.ingredient_repo = ingredient_repo

    async def execute(self, ingredient_id: UUID) -> None:
        ingredient = await self.ingredient_repo.get_by_id(ingredient_id)

        if not ingredient:
            raise ValueError("Ingredient not found")

        await self.ingredient_repo.delete(ingredient_id)
