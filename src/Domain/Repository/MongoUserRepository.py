from typing import Optional
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorCollection
from src.Domain.Entity.User import User, UserRole
from src.Domain.Repository.UserRepository import UserRepository

class MongoUserRepository(UserRepository):
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def find_by_email(self, email: str) -> Optional[User]:
        document = await self.collection.find_one({"email": email})
        if not document:
            return None
        return self._map_to_entity(document)

    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        document = await self.collection.find_one({"_id": str(user_id)})
        if not document:
            return None
        return self._map_to_entity(document)

    async def save(self, user: User) -> None:
        document = self._map_to_document(user)
        await self.collection.replace_one(
            {"_id": document["_id"]},
            document,
            upsert=True
        )

    def _map_to_entity(self, document) -> User:
        return User(
            id=UUID(document["_id"]),
            email=document["email"],
            hashed_password=document["hashed_password"],
            full_name=document.get("full_name"),
            is_active=document.get("is_active", True),
            role=UserRole(document.get("role", UserRole.USER.value))
        )

    def _map_to_document(self, user: User) -> dict:
        return {
            "_id": str(user.id),
            "email": user.email,
            "hashed_password": user.hashed_password,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "role": user.role.value
        }