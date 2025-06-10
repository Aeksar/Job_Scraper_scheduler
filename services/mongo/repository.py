from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from pymongo import MongoClient
from pymongo.database import Database
from typing import Optional
from bson.objectid import ObjectId

from config import logger
 
 
class SubscribeCollection:
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.db = self.client["job_name"]
        self.collection = self.db["subscribe"]
    
    async def get_subscribers(self, text: str, city: str) -> list:
        filter = {"text": text, "city": city}
        doc = await self.collection.find_one(filter)
        if doc:
            return doc["subscriber_ids"]
        
    async def get_params(self) -> list[str]:
        include = {"text": 1, "city": 1, "_id": 0}
        return await self.collection.find({}, include).to_list()
    
    
class HhCollection:
    def __init__(self, client: AsyncIOMotorClient):
        self.db = client["job_name"]
        self.collection = self.db["hh"]
    
    async def find_by_ids(self, ids: list[str]) -> list[dict]:
        valid_ids = []
        for id in ids:
            valid_ids.append(ObjectId(id))
        return await self.collection.find({"_id": {"$in": valid_ids}}, {"_id": 0}).to_list()
    
    async def get_urls(self) -> list[str]:
        return await self.collection.distinct("url")
    
    async def delete_by_urls(self, urls: list[str]):
        res = await self.collection.delete_many({"url": {"$in": urls}})
        logger.info(f"Deleted {res.deleted_count} document by url")