import asyncio
from uuid import uuid4
from src.Infrastructure.Persistence.MongoClient import MongoClient
from src.Infrastructure.Security.JwtAuthService import JwtAuthService


async def create_admin():
    client = MongoClient()
    auth_service = JwtAuthService()
    collection = client.get_collection("users")

    email = "admin@bytebite.com"
    password = "change_me_123"

    user_document = {
        "_id": str(uuid4()),
        "email": email,
        "hashed_password": auth_service.hash_password(password),
        "full_name": "ByteBite Admin",
        "is_active": True
    }

    await collection.update_one(
        {"email": email},
        {"$set": user_document},
        upsert=True
    )
    print(f"User {email} created/updated successfully.")


if __name__ == "__main__":
    asyncio.run(create_admin())