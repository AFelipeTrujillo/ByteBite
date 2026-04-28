import asyncio
from uuid import uuid4
from src.Domain.ValueObject.Category import Category
from src.Infrastructure.Persistence.MongoClient import MongoClient

async def seed():
    client = MongoClient()
    # Ensure this matches your MongoClient implementation (e.g., client.db['ingredients'])
    collection = client.get_collection('ingredients')

    ingredients = [
        # PANTRY
        {"_id": str(uuid4()), "name": "Flour", "category": Category.PANTRY.value},
        {"_id": str(uuid4()), "name": "Pasta", "category": Category.PANTRY.value},
        {"_id": str(uuid4()), "name": "Olive Oil", "category": Category.PANTRY.value},
        {"_id": str(uuid4()), "name": "Rice", "category": Category.PANTRY.value},
        {"_id": str(uuid4()), "name": "Sugar", "category": Category.PANTRY.value},
        {"_id": str(uuid4()), "name": "Bread", "category": Category.PANTRY.value},
        {"_id": str(uuid4()), "name": "Canned Tomatoes", "category": Category.PANTRY.value},
        {"_id": str(uuid4()), "name": "Chickpeas", "category": Category.PANTRY.value},
        {"_id": str(uuid4()), "name": "Lentils", "category": Category.PANTRY.value},
        {"_id": str(uuid4()), "name": "Vinegar", "category": Category.PANTRY.value},
        {"_id": str(uuid4()), "name": "Soy Sauce", "category": Category.PANTRY.value},
        {"_id": str(uuid4()), "name": "Honey", "category": Category.PANTRY.value},
        # DAIRY & EGGS
        {"_id": str(uuid4()), "name": "Egg", "category": Category.DAIRY_EGGS.value},
        {"_id": str(uuid4()), "name": "Milk", "category": Category.DAIRY_EGGS.value},
        {"_id": str(uuid4()), "name": "Butter", "category": Category.DAIRY_EGGS.value},
        {"_id": str(uuid4()), "name": "Cheese", "category": Category.DAIRY_EGGS.value},
        {"_id": str(uuid4()), "name": "Yogurt", "category": Category.DAIRY_EGGS.value},
        {"_id": str(uuid4()), "name": "Cream", "category": Category.DAIRY_EGGS.value},
        # MEAT & FISH
        {"_id": str(uuid4()), "name": "Chicken Breast", "category": Category.MEAT_FISH.value},
        {"_id": str(uuid4()), "name": "Ground Beef", "category": Category.MEAT_FISH.value},
        {"_id": str(uuid4()), "name": "Bacon", "category": Category.MEAT_FISH.value},
        {"_id": str(uuid4()), "name": "Salmon", "category": Category.MEAT_FISH.value},
        {"_id": str(uuid4()), "name": "Tuna", "category": Category.MEAT_FISH.value},
        {"_id": str(uuid4()), "name": "Shrimp", "category": Category.MEAT_FISH.value},
        # VEGETABLES & GREENS
        {"_id": str(uuid4()), "name": "Tomato", "category": Category.VEGETABLES.value},
        {"_id": str(uuid4()), "name": "Garlic", "category": Category.VEGETABLES.value},
        {"_id": str(uuid4()), "name": "Onion", "category": Category.VEGETABLES.value},
        {"_id": str(uuid4()), "name": "Potato", "category": Category.VEGETABLES.value},
        {"_id": str(uuid4()), "name": "Carrot", "category": Category.VEGETABLES.value},
        {"_id": str(uuid4()), "name": "Bell Pepper", "category": Category.VEGETABLES.value},
        {"_id": str(uuid4()), "name": "Lettuce", "category": Category.VEGETABLES.value},
        {"_id": str(uuid4()), "name": "Spinach", "category": Category.VEGETABLES.value},
        {"_id": str(uuid4()), "name": "Broccoli", "category": Category.VEGETABLES.value},
        {"_id": str(uuid4()), "name": "Zucchini", "category": Category.VEGETABLES.value},
        {"_id": str(uuid4()), "name": "Mushroom", "category": Category.VEGETABLES.value},
        {"_id": str(uuid4()), "name": "Cucumber", "category": Category.VEGETABLES.value},
        # HERBS & SPICES
        {"_id": str(uuid4()), "name": "Salt", "category": Category.SPICES.value},
        {"_id": str(uuid4()), "name": "Black Pepper", "category": Category.SPICES.value},
        {"_id": str(uuid4()), "name": "Paprika", "category": Category.SPICES.value},
        {"_id": str(uuid4()), "name": "Oregano", "category": Category.SPICES.value},
        {"_id": str(uuid4()), "name": "Cumin", "category": Category.SPICES.value},
        {"_id": str(uuid4()), "name": "Bay Leaves", "category": Category.SPICES.value},
        {"_id": str(uuid4()), "name": "Cinnamon", "category": Category.SPICES.value},
        {"_id": str(uuid4()), "name": "Turmeric", "category": Category.SPICES.value},
        # FRESH FRUITS
        {"_id": str(uuid4()), "name": "Lemon", "category": Category.FRUITS.value},
        {"_id": str(uuid4()), "name": "Banana", "category": Category.FRUITS.value},
        {"_id": str(uuid4()), "name": "Apple", "category": Category.FRUITS.value},
        {"_id": str(uuid4()), "name": "Avocado", "category": Category.FRUITS.value},
        # FROZEN FOODS
        {"_id": str(uuid4()), "name": "Frozen Peas", "category": Category.FROZEN.value},
        {"_id": str(uuid4()), "name": "Frozen Corn", "category": Category.FROZEN.value},
        {"_id": str(uuid4()), "name": "Ice Cream", "category": Category.FROZEN.value},
    ]

    await collection.delete_many({})
    await collection.insert_many(ingredients)

    print(f"Successfully seeded {len(ingredients)} ingredients.")

if __name__ == "__main__":
    asyncio.run(seed())