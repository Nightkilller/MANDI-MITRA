import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

async def setup_mongodb():
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DB_NAME", "mandimitra")
    
    logger.info(f"Connecting to MongoDB at {uri}...")
    client = AsyncIOMotorClient(uri)
    db = client[db_name]
    
    # 1. Prices Collection
    await db.prices.create_index([("crop", 1), ("mandi", 1), ("date", -1)], unique=False)
    logger.info("Created index on 'prices' collection")

    # 2. Weather Collection
    await db.weather.create_index([("mandi", 1), ("date", -1)], unique=True)
    logger.info("Created index on 'weather' collection")

    # 3. Predictions Collection
    await db.predictions.create_index([("crop", 1), ("mandi", 1), ("created_at", -1)], unique=False)
    logger.info("Created index on 'predictions' collection")

    logger.info("Database setup complete.")

if __name__ == "__main__":
    asyncio.run(setup_mongodb())
