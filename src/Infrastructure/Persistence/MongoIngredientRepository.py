from typing import Optional, List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorCollection

from src.Domain.Entity.Ingredient import Ingredient
from src.Domain.Repository.IngredientRepository import IngredientRepository
from src.Domain.ValueObject.Category import Category


class MongoIngredientRepository(IngredientRepository):


    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def list_all(self) -> List[Ingredient]:
        cursor = self.collection.find()
        return [self._map_to_entity(doc) async for doc in cursor]

    async def get_name_by_id(self, ingredient_id: UUID) -> str:
        doc = await self.collection.find_one(
            {"_id": str(ingredient_id)},
            {"name": 1}
        )

        if not doc:
            return "Unknown Ingredient"

        return doc["name"]

    async def get_by_id(self, ingredient_id: UUID) -> Optional[Ingredient]:
        doc = await self.collection.find_one({"_id": str(ingredient_id)})

        if not doc:
            return None

        return self._map_to_entity(doc)

    async def find_by_name(self, name: str) -> Optional[Ingredient]:
        doc = await self.collection.find_one(
            {"name": {"$regex": f"^{name}$", "$options": "i"}}
        )
        if not doc:
            return None
        return self._map_to_entity(doc)

    async def save(self, ingredient: Ingredient) -> None:
        document = self._map_to_document(ingredient)
        await self.collection.insert_one(document)

    async def update(self, ingredient: Ingredient) -> None:
        document = self._map_to_document(ingredient)
        await self.collection.replace_one(
            {"_id": document["_id"]},
            document
        )

    async def delete(self, ingredient_id: UUID) -> None:
        await self.collection.delete_one({"_id": str(ingredient_id)})

    def _map_to_entity(self, doc):
        return Ingredient(
            id          =UUID(doc["_id"]),
            name        =doc["name"],
            category    =Category(doc["category"])
        )

    def _map_to_document(self, ingredient: Ingredient) -> dict:
        return {
            "_id": str(ingredient.id),
            "name": ingredient.name,
            "category": ingredient.category.value,
        }
