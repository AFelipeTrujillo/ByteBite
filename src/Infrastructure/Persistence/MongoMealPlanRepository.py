from typing import Optional, List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorCollection

from src.Domain.Entity.MealPlan import MealPlan, DailyPlan
from src.Domain.Repository.MealPlanRepository import MealPlanRepository


class MongoMealPlanRepository(MealPlanRepository):

    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def get_by_id(self, meal_plan_id: UUID) -> Optional[MealPlan]:
        doc = await self.collection.find_one({"_id": str(meal_plan_id)})
        if not doc:
            return None

        return self._map_to_entity(doc)

    async def find_by_owner(self, owner_id: UUID) -> List[MealPlan]:
        cursor = self.collection.find(
            {"owner_id": str(owner_id)}
        ).sort([("year", -1), ("week_number", -1)])

        meal_plans = []
        async for doc in cursor:
            meal_plans.append(self._map_to_entity(doc))
        return meal_plans

    async def save(self, meal_plan: MealPlan) -> None:
        document = self._map_to_document(meal_plan)
        await self.collection.replace_one(
            {"_id": document["_id"]},
            document,
            upsert=True
        )

    def _map_to_entity(self, doc):
        days_dict = {}

        for day_index, plan_data in doc.get('days', {}).items():
            days_dict[int(day_index)] = DailyPlan(
                lunch_recipe_id=UUID(plan_data["lunch_recipe_id"]) if plan_data.get("lunch_recipe_id") else None,
                dinner_recipe_id=UUID(plan_data["dinner_recipe_id"]) if plan_data.get("dinner_recipe_id") else None
            )

        return MealPlan(
            id=UUID(doc["_id"]),
            owner_id=UUID(doc["owner_id"]),
            year=doc["year"],
            week_number=doc["week_number"],
            days=days_dict
        )

    def _map_to_document(self, meal_plan: MealPlan) -> dict:
        days_to_store = {}
        for day_index, plan in meal_plan.days.items():
            days_to_store[str(day_index)] = {
                "lunch_recipe_id": str(plan.lunch_recipe_id) if plan.lunch_recipe_id else None,
                "dinner_recipe_id": str(plan.dinner_recipe_id) if plan.dinner_recipe_id else None
            }

        return {
            "_id": str(meal_plan.id),
            "owner_id": str(meal_plan.owner_id),
            "year": meal_plan.year,
            "week_number": meal_plan.week_number,
            "days": days_to_store
        }
