from fastapi import FastAPI

from src.Application.UseCase.GenerateShoppingList import GenerateShoppingList
from src.Infrastructure.Configs.Settings import settings
from src.Infrastructure.Persistence.MongoClient import MongoClient
from src.Infrastructure.DependencyInjection.MongoProviders import get_generate_shopping_list_use_case
from src.Infrastructure.Delivery.Http.ShoppingListController import router as shopping_list_router
from src.Infrastructure.Delivery.Http.AuthController import router as auth_router

app = FastAPI(
    title       =   settings.APP_NAME,
    description =   settings.APP_DESCRIPTION,
    version     =   settings.APP_VERSION
)

mongo_client = MongoClient()

app.dependency_overrides[GenerateShoppingList] = get_generate_shopping_list_use_case

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(shopping_list_router, prefix = "/api/v1", tags=["Shopping List"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "database": "connected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main.app", host="0.0.0.0", port=8000, reload=True)
