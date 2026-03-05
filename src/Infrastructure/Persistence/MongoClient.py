import os
from motor.motor_asyncio import AsyncIOMotorClient

from src.Infrastructure.Configs.Settings import settings

class MongoClient:

    def __init__(self):
        mongo_uri = settings.MONGO_URI
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db = self.client[settings.MONGO_DB_NAME]

    def get_collection(self, name: str):
        return self.db[name]