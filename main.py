from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.Application.UseCase.GenerateShoppingList import GenerateShoppingList
from src.Infrastructure.Configs.Settings import settings, Settings
from src.Infrastructure.Persistence.MongoClient import MongoClient
from src.Infrastructure.DependencyInjection.MongoProviders import get_generate_shopping_list_use_case
from src.Infrastructure.Delivery.Http.ShoppingListController import router as shopping_list_router
from src.Infrastructure.Delivery.Http.AuthController import router as auth_router
from src.Infrastructure.Delivery.Http.MealPlanController import router as meal_plan_router
from src.Infrastructure.Delivery.Http.RecipeController import router as recipe_router

app = FastAPI(
    title       =   settings.APP_NAME,
    description =   settings.APP_DESCRIPTION,
    version     =   settings.APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=[settings.FRONT_END_URL],
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo_client = MongoClient()

app.dependency_overrides[GenerateShoppingList] = get_generate_shopping_list_use_case

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(shopping_list_router, prefix = "/api/v1", tags=["Shopping List"])
app.include_router(meal_plan_router, prefix="/api/v1", tags=["Meal Planning"])
app.include_router(recipe_router, prefix="/api/v1", tags=["Recipes"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "database": "connected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main.app", host="0.0.0.0", port=8000, reload=True)
