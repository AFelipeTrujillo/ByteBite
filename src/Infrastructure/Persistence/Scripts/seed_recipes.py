import asyncio
from uuid import uuid4, UUID
from typing import Optional
from src.Infrastructure.Persistence.MongoClient import MongoClient
from src.Domain.Entity.Recipe import Recipe, RecipeIngredient
from src.Domain.ValueObject.Unit import Unit
from src.Domain.ValueObject.IngredientQuantity import IngredientQuantity


async def seed_recipes():
    client = MongoClient()
    db = client.db
    ingredients_col = db["ingredients"]
    recipes_col = db["recipes"]

    async def get_ingredient_id(name: str) -> Optional[UUID]:
        # Searching by exact English name
        doc = await ingredients_col.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
        if doc:
            return UUID(doc["_id"]) if isinstance(doc["_id"], str) else doc["_id"]
        return None

    print("Searching for ingredients in database...")

    # Matching names from your updated seed_ingredients.py
    pasta_id = await get_ingredient_id("Pasta")
    tomato_id = await get_ingredient_id("Tomato")
    oil_id = await get_ingredient_id("Olive Oil")
    garlic_id = await get_ingredient_id("Garlic")

    if not pasta_id or not tomato_id:
        print("Error: Base ingredients not found. Please run seed_ingredients first.")
        return

    sample_recipe = Recipe(
        id=uuid4(),
        owner_id=uuid4(),
        name="Pasta Express",
        ingredients=[
            RecipeIngredient(
                ingredient_id=pasta_id,
                quantity=IngredientQuantity(amount=100, unit=Unit.GRAMS)
            ),
            RecipeIngredient(
                ingredient_id=tomato_id,
                quantity=IngredientQuantity(amount=2, unit=Unit.UNITS)
            ),
            RecipeIngredient(
                ingredient_id=oil_id,
                quantity=IngredientQuantity(amount=10, unit=Unit.MILLILITERS)
            ),
            RecipeIngredient(
                ingredient_id=garlic_id,
                quantity=IngredientQuantity(amount=1, unit=Unit.CLOVE)
            )
        ],
        references=["https://recipes.com/pasta-express"],
        invited_users=[]
    )

    def recipe_to_dict(r: Recipe):
        return {
            "_id": str(r.id),
            "owner_id": str(r.owner_id),
            "name": r.name,
            "references": r.references,
            "invited_users": [str(u) for u in r.invited_users],
            "ingredients": [
                {
                    "ingredient_id": str(ri.ingredient_id),
                        "quantity": {
                        "value": ri.quantity.amount,
                        "unit": ri.quantity.unit.value
                    }
                } for ri in r.ingredients
            ]
        }

    print(f"Inserting recipe: {sample_recipe.name}...")
    await recipes_col.update_one(
        {"name": sample_recipe.name},
        {"$set": recipe_to_dict(sample_recipe)},
        upsert=True
    )

    print(f"Recipe '{sample_recipe.name}' created successfully.")
    print(f"Recipe ID: {sample_recipe.id}")


if __name__ == "__main__":
    asyncio.run(seed_recipes())