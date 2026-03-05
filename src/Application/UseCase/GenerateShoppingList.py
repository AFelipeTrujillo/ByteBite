from uuid import UUID
from typing import List, Dict

from src.Domain.ValueObject.IngredientQuantity import IngredientQuantity
from src.Domain.Repository.RecipeRepository import RecipeRepository
from src.Domain.Repository.MealPlanRepository import MealPlanRepository
from src.Domain.Repository.IngredientRepository import IngredientRepository
from src.Application.DTO.ShoppingListItem import ShoppingListItem



class GenerateShoppingList:

    def __init__(
            self,
            meal_plan_repo: MealPlanRepository,
            recipe_repo: RecipeRepository,
            ingredient_repo: IngredientRepository
    ):
        self.meal_plan_repo = meal_plan_repo
        self.recipe_repo = recipe_repo
        self.ingredient_repo = ingredient_repo

    async def execute(self, meal_plan_id: UUID) -> List[ShoppingListItem]:
        meal_plan = await self.meal_plan_repo.get_by_id(meal_plan_id)
        if not meal_plan:
            raise ValueError("Meal Plan not found")

        recipe_ids = set()
        for day in meal_plan.days.values():
            if day.lunch_recipe_id:
                recipe_ids.add(day.lunch_recipe_id)
            if day.dinner_recipe_id:
                recipe_ids.add(day.dinner_recipe_id)

        recipes = await self.recipe_repo.get_by_ids(list(recipe_ids))
        totals: Dict[UUID, IngredientQuantity] = {}

        for recipe in recipes:
            for item in recipe.ingredients:
                if item.ingredient_id in totals:
                    totals[item.ingredient_id] += item.quantity
                else:
                    totals[item.ingredient_id] = item.quantity

        response: List[ShoppingListItem] = []
        for ing_id, quantity in totals.items():
            name = await self.ingredient_repo.get_name_by_id(ing_id)
            response.append(
                ShoppingListItem(
                    ingredient_id=ing_id,
                    ingredient_name=name,
                    amount=quantity.amount,
                    unit=quantity.unit
                )
            )
        return response