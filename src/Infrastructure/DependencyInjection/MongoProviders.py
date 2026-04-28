from fastapi.params import Depends

from src.Application.UseCase.CreateMealPlan import CreateMealPlan
from src.Application.UseCase.LoginUseCase import LoginUseCase
from src.Application.UseCase.RegisterUseCase import RegisterUseCase
from src.Application.UseCase.CreateRecipeUseCase import CreateRecipeUseCase
from src.Application.UseCase.GetRecipeByIdUseCase import GetRecipeByIdUseCase
from src.Application.UseCase.UpdateRecipeUseCase import UpdateRecipeUseCase
from src.Application.UseCase.DeleteRecipeUseCase import DeleteRecipeUseCase
from src.Domain.Repository.MongoUserRepository import MongoUserRepository
from src.Infrastructure.Persistence.MongoClient import MongoClient
from src.Infrastructure.Persistence.MongoRecipeRepository import MongoRecipeRepository
from src.Infrastructure.Persistence.MongoMealPlanRepository import MongoMealPlanRepository
from src.Infrastructure.Persistence.MongoIngredientRepository import MongoIngredientRepository
from src.Application.UseCase.GenerateShoppingList import GenerateShoppingList
from src.Infrastructure.Security.JwtAuthService import JwtAuthService
from src.Application.UseCase.GetRecipesUseCase import GetRecipesUseCase

db_client = MongoClient()


def get_generate_shopping_list_use_case() -> GenerateShoppingList:

    recipe_repo = MongoRecipeRepository(db_client.get_collection("recipes"))
    meal_plan_repo = MongoMealPlanRepository(db_client.get_collection("meal_plans"))
    ingredient_repo = MongoIngredientRepository(db_client.get_collection("ingredients"))


    return GenerateShoppingList(meal_plan_repo, recipe_repo, ingredient_repo)


def get_login_use_case() -> LoginUseCase:
    user_repo = MongoUserRepository(db_client.get_collection("users"))
    auth_service = JwtAuthService()

    return LoginUseCase(user_repo, auth_service)


def get_register_use_case() -> RegisterUseCase:
    user_repo = MongoUserRepository(db_client.get_collection("users"))
    auth_service = JwtAuthService()

    return RegisterUseCase(user_repo, auth_service)


def get_meal_plan_repository() -> MongoMealPlanRepository:
    return MongoMealPlanRepository(db_client.db["meal_plans"])

def get_create_meal_plan_use_case(
    repo: MongoMealPlanRepository = Depends(get_meal_plan_repository)
) -> CreateMealPlan:
    return CreateMealPlan(repo)

def get_get_recipes_use_case():
    repository = MongoRecipeRepository(db_client.get_collection("recipes"))
    return GetRecipesUseCase(repository)

def get_recipe_repository() -> MongoRecipeRepository:
    return MongoRecipeRepository(db_client.get_collection("recipes"))

def get_create_recipe_use_case(
    repo: MongoRecipeRepository = Depends(get_recipe_repository)
) -> CreateRecipeUseCase:
    return CreateRecipeUseCase(repo)

def get_get_recipe_by_id_use_case(
    repo: MongoRecipeRepository = Depends(get_recipe_repository)
) -> GetRecipeByIdUseCase:
    return GetRecipeByIdUseCase(repo)

def get_update_recipe_use_case(
    repo: MongoRecipeRepository = Depends(get_recipe_repository)
) -> UpdateRecipeUseCase:
    return UpdateRecipeUseCase(repo)

def get_delete_recipe_use_case(
    repo: MongoRecipeRepository = Depends(get_recipe_repository)
) -> DeleteRecipeUseCase:
    return DeleteRecipeUseCase(repo)
