import asyncio
from uuid import uuid4
from src.Domain.ValueObject.Category import Category
from src.Infrastructure.Persistence.MongoClient import MongoClient

async def seed():
    client = MongoClient()
    # Ensure this matches your MongoClient implementation (e.g., client.db['ingredients'])
    collection = client.get_collection('ingredients')

    ingredients = [
        {"_id": str(uuid4()), "name": "Flour", "category": Category.PANTRY.value},
        {"_id": str(uuid4()), "name": "Egg", "category": Category.DAIRY_EGGS.value},
        {"_id": str(uuid4()), "name": "Salt", "category": Category.SPICES.value},
        {"_id": str(uuid4()), "name": "Tomato", "category": Category.VEGETABLES.value},
        {"_id": str(uuid4()), "name": "Pasta", "category": Category.PANTRY.value},
        {"_id": str(uuid4()), "name": "Olive Oil", "category": Category.PANTRY.value},
        {"_id": str(uuid4()), "name": "Garlic", "category": Category.VEGETABLES.value},
    ]

    await collection.delete_many({})
    await collection.insert_many(ingredients)

    print(f"Successfully seeded {len(ingredients)} ingredients.")

if __name__ == "__main__":
    asyncio.run(seed())