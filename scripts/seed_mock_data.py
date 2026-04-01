"""
Seed MongoDB with mock data for local testing.
Run: python scripts/seed_mock_data.py
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/mandimitra")
DB_NAME = os.getenv("MONGODB_DB_NAME", "mandimitra")

async def seed_data():
    print(f"Connecting to {MONGODB_URI}...")
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    
    crops = ["tomato", "onion", "wheat", "soybean"]
    mandis = ["indore", "bhopal", "ujjain"]
    
    docs = []
    base_prices = {"tomato": 2500, "onion": 1800, "wheat": 2200, "soybean": 4500}
    
    for crop in crops:
        for mandi in mandis:
            current_price = base_prices[crop]
            for i in range(100):
                date = datetime.now() - timedelta(days=100-i)
                # Random walk
                current_price += random.uniform(-50, 50)
                docs.append({
                    "date": date,
                    "crop": crop,
                    "mandi": mandi,
                    "min_price": round(current_price * 0.9, 2),
                    "max_price": round(current_price * 1.1, 2),
                    "modal_price": round(current_price, 2),
                    "arrival_tonnes": round(random.uniform(500, 1500), 2)
                })
    
    if docs:
        print(f"Inserting {len(docs)} mock records...")
        await db.prices.insert_many(docs)
        print("Done!")

if __name__ == "__main__":
    asyncio.run(seed_data())
