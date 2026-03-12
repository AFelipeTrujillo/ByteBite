from uuid import uuid4
from src.Domain.Entity.Recipe import Recipe, RecipeIngredient
from src.Domain.ValueObject.IngredientQuantity import IngredientQuantity
from src.Domain.ValueObject.Unit import Unit


def test_recipe_entity_validation():
    # Arrange
    recipe_id = uuid4()
    owner_id = uuid4()
    pasta_id = uuid4()

    # Act
    recipe = Recipe(
        id=recipe_id,
        owner_id=owner_id,
        name="Test Recipe",
        ingredients=[
            RecipeIngredient(
                ingredient_id=pasta_id,
                quantity=IngredientQuantity(amount=500, unit=Unit.GRAMS)
            )
        ]
    )

    # Assert
    assert recipe.name == "Test Recipe"
    assert isinstance(recipe.ingredients[0].quantity.unit, Unit)
    assert recipe.ingredients[0].quantity.amount == 500
    assert recipe.ingredients[0].ingredient_id == pasta_id