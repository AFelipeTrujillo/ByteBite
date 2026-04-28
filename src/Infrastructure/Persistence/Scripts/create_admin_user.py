import asyncio
import os
from uuid import uuid4
from src.Infrastructure.Persistence.MongoClient import MongoClient
from src.Infrastructure.Security.JwtAuthService import JwtAuthService
from src.Domain.Entity.User import UserRole


async def create_admin():
    client = MongoClient()
    auth_service = JwtAuthService()

    db = client.db
    collection = db["users"]

    email = "admin@bytebite.com"
    password = "change_me_123"

    print(f"Hashing password for {email}...")

    try:

        hashed = auth_service.hash_password(password)

        user_document = {
            "_id": str(uuid4()),
            "email": email,
            "hashed_password": hashed,
            "full_name": "ByteBite Admin",
            "is_active": True,
            "role": UserRole.ADMIN.value
        }


        result = await collection.update_one(
            {"email": email},
            {"$set": user_document},
            upsert=True
        )

        if result.upserted_id:
            print(f"User {email} created successfully.")
        else:
            print(f"User {email} updated successfully.")

    except ValueError as e:
        print(f"Error de hashing: {e}")


if __name__ == "__main__":
    asyncio.run(create_admin())