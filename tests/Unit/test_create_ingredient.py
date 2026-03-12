import pytest
from uuid import uuid4

from src.Domain.Entity.Ingredient import Ingredient
from src.Domain.ValueObject.Category import Category


async def test_create_ingredient():

    ingredient1 = Ingredient(
        id      = uuid4(),
        name    = "Apple",
        category    = Category.FRUITS.value
    )

    assert ingredient1.name == "Apple"
    assert ingredient1.category == 106
