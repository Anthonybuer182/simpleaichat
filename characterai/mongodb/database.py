# database.py
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase

client: AsyncIOMotorClient = None

async def init_db(uri: str) -> AsyncIOMotorDatabase:
    global client
    if client is None:
        client = AsyncIOMotorClient(uri)
    return client["conversation_database"]

async def close_db():
    global client
    if client:
        client.close()

async def get_db() -> AsyncIOMotorDatabase:
    if client is None:
        raise RuntimeError("Database client is not initialized.")
    return client["conversation_database"]
