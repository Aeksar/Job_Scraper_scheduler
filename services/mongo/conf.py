from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

from config import mongo_cfg, logger


def sync_connect_to_mongo():
    try:
        client = MongoClient(mongo_cfg.url())
        logger.info("Successful connect to mongo")
        return client
    except Exception as e:
        logger.info(f"Error connecting to mongo: {e}")
        return None

mongo_client = sync_connect_to_mongo()