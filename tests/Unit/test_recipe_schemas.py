import pytest
from uuid import uuid4
from src.Infrastructure.Delivery.Http.Schemas.RecipeSchema import IngredientQuantitySchema, RecipeResponse
from src.Domain.ValueObject.Unit import Unit


def test_ingredient_quantity_schema_serialization():

    data = {
        "amount": 500.0,
        "unit": Unit.GRAMS  # Domain Enum object
    }

    schema = IngredientQuantitySchema.model_validate(data)

    assert schema.amount == 500.0
    assert schema.unit == "GRAMS"  # Verify the validator's transformation
    assert isinstance(schema.unit, str)


def test_recipe_response_serialization():

    recipe_id = uuid4()
    owner_id = uuid4()
    ingredient_id = uuid4()


    recipe_data = {
        "id": recipe_id,
        "owner_id": owner_id,
        "name": "Chicken and Rice",
        "ingredients": [
            {
                "ingredient_id": ingredient_id,
                "quantity": {"amount": 200, "unit": Unit.GRAMS}
            }
        ],
        "references": ["http://culinary_manual.com"]
    }

    response = RecipeResponse.model_validate(recipe_data)

    assert response.name == "Chicken and Rice"
    assert response.ingredients[0].quantity.unit == "GRAMS"