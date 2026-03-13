from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorCollection

from src.Domain.Entity.Recipe import Recipe, RecipeIngredient
from src.Domain.Repository.RecipeRepository import RecipeRepository
from src.Domain.ValueObject.IngredientQuantity import IngredientQuantity
from src.Domain.ValueObject.Unit import Unit


class MongoRecipeRepository(RecipeRepository):

    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def get_by_ids(self, ids: List[UUID]) -> List[Recipe]:
        string_ids = [str(i) for i in ids]

        cursor = self.collection.find({"_id": {"$in": string_ids}})
        recipes = []

        async for doc in cursor:
            recipes.append(self._map_to_entity(doc))

        return recipes

    async def find_by_owner(self, owner_id: UUID) -> List[Recipe]:
        cursor = self.collection.find({"owner_id": str(owner_id)})
        recipes = []

        async for doc in cursor:
            recipes.append(self._map_to_entity(doc))

        return recipes

    def _map_to_entity(self, doc: dict) -> Recipe:

        return Recipe(
            id          = UUID(doc['_id']),
            owner_id    = UUID(doc["owner_id"]),
            name        = doc["name"],
            ingredients = [
                RecipeIngredient(
                    ingredient_id=UUID(item["ingredient_id"]),
                    quantity=IngredientQuantity(
                        amount=item["quantity"]["value"],
                        unit=Unit(item["quantity"]["unit"])
                    )
                ) for item in doc["ingredients"]
            ],
            references  = doc.get("references", [])
        )
