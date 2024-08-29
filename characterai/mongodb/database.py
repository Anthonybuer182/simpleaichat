# database.py
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# 全局数据库客户端
client: AsyncIOMotorClient = None

async def init_db(uri: str, db_name: str):
    global client
    client = AsyncIOMotorClient(uri)
    return client[db_name]

async def close_db():
    global client
    client.close()
