import asyncio
from uuid import uuid4

from src.Domain.ValueObject.Category import Category
from src.Infrastructure.Persistence.MongoClient import MongoClient


async def seed():
    client = MongoClient()
    collection = client.get_collection('ingredients')

    ingredients = [
        {"_id": uuid4(), "name": "Flour", "category": Category.PANTRY.value},
        {"_id": uuid4(), "name": "Egg", "category": Category.DAIRY_EGGS.value},
        {"_id": uuid4(), "name": "Salt", "category": Category.SPICES.value},
        {"_id": uuid4(), "name": "Tomato", "category": Category.VEGETABLES.value},
    ]

    await collection.delete_many({})
    await collection.insert_many(ingredients)

    print("Ingredients created")

if __name__ == "__main__":
    asyncio.run(seed())