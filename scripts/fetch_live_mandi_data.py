"""
Fetch real-time daily agricultural market prices from data.gov.in (Agmarknet)
and store them in SQLite for the MandiMitra XAI platform.

Strategy: Filter by state=MP + commodity only (no market/district filter)
to maximize data capture. Then map records to our internal mandi IDs by district.

Run: python scripts/fetch_live_mandi_data.py
"""
import asyncio
import httpx
import sqlite3
import logging
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

AGMARKNET_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "mandimitra.db")

# Commodity names as they appear in data.gov.in API
CROP_MAP = {
    "tomato": "Tomato",
    "onion": "Onion",
    "wheat": "Wheat",
    "soybean": "Soyabean",
    "garlic": "Garlic",
    "potato": "Potato",
    "mustard": "Mustard",
    "gram": "Gram",
    "maize": "Maize",
    "cotton": "Cotton",
}

# Map data.gov.in district names → our internal mandi IDs
DISTRICT_TO_MANDI = {
    "indore": "indore",
    "bhopal": "bhopal",
    "ujjain": "ujjain",
    "jabalpur": "jabalpur",
    "sagar": "sagar",
    "gwalior": "gwalior",
    "mandsaur": "mandsaur",
    "khargone": "khargone",
    "vidisha": "vidisha",
    "hoshangabad": "hoshangabad",
    "narmadapuram": "hoshangabad",  # Renamed district
}


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            crop TEXT NOT NULL,
            mandi TEXT NOT NULL,
            min_price REAL DEFAULT 0,
            max_price REAL DEFAULT 0,
            modal_price REAL DEFAULT 0,
            arrival_tonnes REAL DEFAULT 0,
            district TEXT DEFAULT '',
            variety TEXT DEFAULT '',
            UNIQUE(date, crop, mandi)
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_crop_mandi_date ON prices(crop, mandi, date)")
    conn.commit()
    conn.close()
    logger.info(f"SQLite database ready at {DB_PATH}")


async def fetch_all_records_for_crop(client: httpx.AsyncClient, crop_id: str, gov_commodity: str):
    """Fetch ALL records for a commodity in MP (no district/market filter for max data)."""
    api_key = settings.DATAGOV_API_KEY
    if not api_key:
        logger.error("DATAGOV_API_KEY is missing in .env")
        return []

    all_records = []
    offset = 0
    limit = 500

    while True:
        params = {
            "api-key": api_key,
            "format": "json",
            "filters[state]": "Madhya Pradesh",
            "filters[commodity]": gov_commodity,
            "limit": limit,
            "offset": offset,
        }

        try:
            response = await client.get(AGMARKNET_URL, params=params, timeout=20.0)
            response.raise_for_status()
            data = response.json()
            records = data.get("records", [])
            total = data.get("total", 0)

            if not records:
                break

            all_records.extend(records)
            logger.info(f"  {crop_id}: fetched {len(all_records)}/{total} records (offset={offset})")

            if len(all_records) >= total or len(records) < limit:
                break

            offset += limit
            await asyncio.sleep(0.5)  # Rate limit
        except httpx.TimeoutException:
            logger.warning(f"  Timeout for {crop_id} at offset={offset}, moving on...")
            break
        except Exception as e:
            logger.error(f"  Error fetching {crop_id}: {e}")
            break

    return all_records


def process_and_insert(conn: sqlite3.Connection, records: list, crop_id: str):
    """Process API records and insert into SQLite. Returns count of inserted records."""
    inserted = 0
    skipped = 0

    for record in records:
        try:
            # Parse date
            date_str = record.get("arrival_date", "")
            dt = datetime.strptime(date_str, "%d/%m/%Y")

            # Parse prices
            min_p = float(record.get("min_price", 0) or 0)
            max_p = float(record.get("max_price", 0) or 0)
            modal_p = float(record.get("modal_price", 0) or 0)

            if modal_p <= 0:
                if min_p > 0 and max_p > 0:
                    modal_p = (min_p + max_p) / 2
                else:
                    skipped += 1
                    continue

            # Map district to our mandi ID
            district = record.get("district", "").strip()
            mandi_id = DISTRICT_TO_MANDI.get(district.lower())

            if not mandi_id:
                # Still store it with district name lowered as mandi
                mandi_id = district.lower().replace(" ", "_") if district else "unknown"

            district_name = district
            variety = record.get("variety", "")

            conn.execute(
                """INSERT INTO prices (date, crop, mandi, min_price, max_price, modal_price, arrival_tonnes, district, variety)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(date, crop, mandi) DO UPDATE SET
                     min_price = excluded.min_price,
                     max_price = excluded.max_price,
                     modal_price = excluded.modal_price""",
                (dt.strftime("%Y-%m-%d"), crop_id, mandi_id,
                 round(min_p, 2), round(max_p, 2), round(modal_p, 2),
                 0.0, district_name, variety)
            )
            inserted += 1
        except ValueError:
            skipped += 1
        except Exception as e:
            skipped += 1

    return inserted, skipped


async def sync_live_data():
    """Main sync: pull all MP commodity data from data.gov.in → SQLite."""
    logger.info("=" * 60)
    logger.info("MandiMitra — Live Market Data Sync from data.gov.in")
    logger.info("=" * 60)

    init_db()
    conn = sqlite3.connect(DB_PATH)
    grand_total_inserted = 0
    grand_total_skipped = 0

    async with httpx.AsyncClient() as http_client:
        for crop_id, gov_commodity in CROP_MAP.items():
            logger.info(f"\n📦 Fetching: {crop_id.upper()} ({gov_commodity})")

            records = await fetch_all_records_for_crop(http_client, crop_id, gov_commodity)

            if records:
                inserted, skipped = process_and_insert(conn, records, crop_id)
                grand_total_inserted += inserted
                grand_total_skipped += skipped
                logger.info(f"  ✅ {crop_id}: {inserted} inserted, {skipped} skipped")
            else:
                logger.warning(f"  ⚠️  No records returned for {crop_id}")

            conn.commit()
            await asyncio.sleep(0.5)

    conn.close()

    # Print summary
    conn = sqlite3.connect(DB_PATH)
    total_rows = conn.execute("SELECT COUNT(*) FROM prices").fetchone()[0]
    unique_crops = conn.execute("SELECT COUNT(DISTINCT crop) FROM prices").fetchone()[0]
    unique_mandis = conn.execute("SELECT COUNT(DISTINCT mandi) FROM prices").fetchone()[0]
    date_range = conn.execute("SELECT MIN(date), MAX(date) FROM prices").fetchone()

    logger.info("\n" + "=" * 60)
    logger.info("✅ SYNC COMPLETE!")
    logger.info(f"   Records inserted/updated: {grand_total_inserted}")
    logger.info(f"   Records skipped: {grand_total_skipped}")
    logger.info(f"   Total in database: {total_rows}")
    logger.info(f"   Crops: {unique_crops}, Mandis: {unique_mandis}")
    if date_range[0]:
        logger.info(f"   Date range: {date_range[0]} → {date_range[1]}")
    logger.info(f"   Database: {DB_PATH}")

    # Show per-mandi breakdown for our tracked mandis
    logger.info("\n📊 Records per tracked mandi:")
    for mandi_id in ["indore", "bhopal", "ujjain", "jabalpur", "sagar", "gwalior", "mandsaur", "khargone", "vidisha", "hoshangabad"]:
        count = conn.execute("SELECT COUNT(*) FROM prices WHERE mandi = ?", (mandi_id,)).fetchone()[0]
        if count > 0:
            logger.info(f"   {mandi_id}: {count} records")

    conn.close()
    logger.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(sync_live_data())
