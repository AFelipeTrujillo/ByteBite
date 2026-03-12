import certifi
from motor.motor_asyncio import AsyncIOMotorClient

from src.Infrastructure.Configs.Settings import settings

class MongoClient:

    def __init__(self):
        self.client = AsyncIOMotorClient(
            settings.MONGO_URI,
            tlsCAFile=certifi.where(),
            uuidRepresentation="standard"
        )
        self.db = self.client[settings.MONGO_DB_NAME]

    def get_collection(self, name: str):
        return self.db[name]