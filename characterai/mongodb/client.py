from motor.motor_asyncio import AsyncIOMotorClient

class MongoDBClient:
    def __init__(self, uri, database_name):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[database_name]

    async def insert_one(self, collection_name, document):
        collection = self.db[collection_name]
        return await collection.insert_one(document)

    async def find_one(self, collection_name, query):
        collection = self.db[collection_name]
        return await collection.find_one(query)

    async def update_one(self, collection_name, query, update):
        collection = self.db[collection_name]
        return await collection.update_one(query, {"$set": update})

    async def delete_one(self, collection_name, query):
        collection = self.db[collection_name]
        return await collection.delete_one(query)

    async def close(self):
        self.client.close()
