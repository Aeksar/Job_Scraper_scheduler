from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from bson.datetime_ms import DatetimeMS

from config import logger, mongo_cfg
 
 
class SubscribeCollection:
    def __init__(self, client: MongoClient):
        self.client = client
        self.db = self.client[mongo_cfg.DATABASE]
        self.collection = self.db["subscribe"]
    
    def get_subscribers(self, text: str, city: str) -> list:
        filter = {"text": text, "city": city}
        doc = self.collection.find_one(filter)
        if doc:
            return doc["subscriber_ids"]
        
    def get_params(self) -> list[str]:
        include = {"text": 1, "city": 1, "_id": 0}
        return self.collection.find({}, include).to_list()
    
    
class HhCollection:
    def __init__(self, client: MongoClient):
        self.db = client[mongo_cfg.DATABASE]
        self.collection = self.db["hh"]
    
    def find_by_ids(self, ids: list[str]) -> list[dict]:
        valid_ids = []
        for id in ids:
            valid_ids.append(ObjectId(id))
        return self.collection.find({"_id": {"$in": valid_ids}}, {"_id": 0}).to_list()
    
    def get_urls(self) -> list[str]:
        return self.collection.distinct("url")
    
    def delete_by_urls(self, urls: list[str]):
        res = self.collection.delete_many({"url": {"$in": urls}})
        logger.info(f"Deleted {res.deleted_count} document by url")
        

class TaskCollection:
    def __init__(self, client: MongoClient):
        self.client = client
        self.db = self.client[mongo_cfg.DATABASE]
        self.collection = self.db["search_result"]
    
    def add(self, params: dict) -> ObjectId:
        res = self.collection.insert_one({
            "status": "pending",
            "parameters": params,
            "created_at": DatetimeMS(datetime.now())
        })
        return res.inserted_id