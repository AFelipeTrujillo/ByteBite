
from src.Infrastructure.Persistence.MongoClient import MongoClient
from src.Infrastructure.Persistence.MongoRecipeRepository import MongoRecipeRepository
from src.Infrastructure.Persistence.MongoMealPlanRepository import MongoMealPlanRepository
from src.Infrastructure.Persistence.MongoIngredientRepository import MongoIngredientRepository
from src.Application.UseCase.GenerateShoppingList import GenerateShoppingList

db_client = MongoClient()


def get_generate_shopping_list_use_case() -> GenerateShoppingList:

    recipe_repo = MongoRecipeRepository(db_client.get_collection("recipes"))
    meal_plan_repo = MongoMealPlanRepository(db_client.get_collection("meal_plans"))
    ingredient_repo = MongoIngredientRepository(db_client.get_collection("ingredients"))


    return GenerateShoppingList(meal_plan_repo, recipe_repo, ingredient_repo)