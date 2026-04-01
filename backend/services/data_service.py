import httpx
import numpy as np
import sqlite3
import os
from datetime import datetime, timedelta
from backend.config import settings
import logging
import hashlib

logger = logging.getLogger(__name__)

# Path for SQLite database file (stored in project root)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "mandimitra.db")

# Realistic base prices per crop (₹ per quintal, based on MP mandi data)
CROP_BASE_PRICES = {
    "tomato": {"base": 1800, "volatility": 400, "seasonal_amp": 600},
    "onion": {"base": 1200, "volatility": 300, "seasonal_amp": 500},
    "wheat": {"base": 2200, "volatility": 80, "seasonal_amp": 150},
    "soybean": {"base": 4200, "volatility": 200, "seasonal_amp": 300},
    "garlic": {"base": 8000, "volatility": 800, "seasonal_amp": 1500},
    "potato": {"base": 1000, "volatility": 200, "seasonal_amp": 350},
    "mustard": {"base": 5500, "volatility": 150, "seasonal_amp": 400},
    "gram": {"base": 4800, "volatility": 180, "seasonal_amp": 350},
    "maize": {"base": 1900, "volatility": 100, "seasonal_amp": 200},
    "cotton": {"base": 6500, "volatility": 250, "seasonal_amp": 500},
}

MANDI_OFFSETS = {
    "indore": 1.05, "bhopal": 1.02, "ujjain": 0.98, "jabalpur": 0.97,
    "sagar": 0.95, "gwalior": 1.00, "mandsaur": 1.03, "khargone": 0.96,
    "vidisha": 0.94, "hoshangabad": 0.99,
}


class DataService:
    def __init__(self):
        self.db_path = DB_PATH
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database and create table if not exists."""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            conn = sqlite3.connect(self.db_path)
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
            logger.info(f"SQLite database ready at {self.db_path}")
        except Exception as e:
            logger.warning(f"SQLite init failed: {e}")

    def _query_prices(self, crop: str, mandi: str, start_date: datetime, end_date: datetime, limit: int) -> list:
        """Query price data from SQLite."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """SELECT date, crop, mandi, min_price, max_price, modal_price, arrival_tonnes
                   FROM prices
                   WHERE crop = ? AND mandi = ? AND date >= ? AND date <= ?
                   ORDER BY date ASC
                   LIMIT ?""",
                (crop, mandi, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), limit)
            )
            rows = cursor.fetchall()
            conn.close()

            prices = []
            for row in rows:
                prices.append({
                    "date": datetime.strptime(row["date"], "%Y-%m-%d"),
                    "crop": row["crop"],
                    "mandi": row["mandi"],
                    "min_price": row["min_price"],
                    "max_price": row["max_price"],
                    "modal_price": row["modal_price"],
                    "arrival_tonnes": row["arrival_tonnes"],
                })
            return prices
        except Exception as e:
            logger.warning(f"SQLite query failed: {e}")
            return []

    def _generate_synthetic_prices(self, crop: str, mandi: str, num_days: int) -> list:
        """Generate realistic synthetic price data for demo/fallback."""
        crop_info = CROP_BASE_PRICES.get(crop, {"base": 2500, "volatility": 200, "seasonal_amp": 300})
        mandi_mult = MANDI_OFFSETS.get(mandi, 1.0)
        seed = int(hashlib.md5(f"{crop}_{mandi}".encode()).hexdigest()[:8], 16)
        rng = np.random.RandomState(seed)

        base_price = crop_info["base"] * mandi_mult
        volatility = crop_info["volatility"]
        seasonal_amp = crop_info["seasonal_amp"]

        prices = []
        current_price = base_price

        for i in range(num_days):
            date = datetime.now() - timedelta(days=num_days - i)
            month_angle = 2 * np.pi * date.timetuple().tm_yday / 365
            seasonal = seasonal_amp * np.sin(month_angle - np.pi / 3)
            weekly = 30 * np.sin(2 * np.pi * date.weekday() / 7)
            shock = rng.randn() * volatility * 0.15
            mean_reversion = 0.05 * (base_price + seasonal - current_price)
            current_price = current_price + shock + mean_reversion + weekly * 0.1
            arrival = max(50, 800 + rng.randn() * 300 + 200 * np.sin(month_angle))

            prices.append({
                "date": date,
                "crop": crop,
                "mandi": mandi,
                "modal_price": round(max(current_price, base_price * 0.5), 2),
                "min_price": round(max(current_price * 0.85, base_price * 0.4), 2),
                "max_price": round(current_price * 1.15, 2),
                "arrival_tonnes": round(arrival, 1),
            })
        return prices

    async def get_features(self, crop: str, mandi: str, lookback_days: int = 30) -> np.ndarray:
        """Fetch and assemble feature matrix for model input. Shape: [lookback_days, n_features]"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=lookback_days + 10)

        # Try SQLite first
        prices = self._query_prices(crop, mandi, start_date, end_date, lookback_days + 10)

        if prices:
            logger.info(f"Loaded {len(prices)} real prices from SQLite for {crop}/{mandi}")
        else:
            logger.info(f"No SQLite data for {crop}/{mandi}. Using synthetic fallback.")
            prices = self._generate_synthetic_prices(crop, mandi, lookback_days + 10)

        # Fetch weather from Open-Meteo (free, no API key)
        weather = await self._fetch_weather(mandi, start_date, end_date)

        # Build feature matrix
        features = self._build_features(prices, weather, lookback_days)
        return features

    async def _fetch_weather(self, mandi: str, start_date: datetime, end_date: datetime) -> dict:
        MANDI_COORDS = {
            "indore": (22.7196, 75.8577), "bhopal": (23.2599, 77.4126),
            "ujjain": (23.1765, 75.7885), "jabalpur": (23.1815, 79.9864),
            "sagar": (23.8388, 78.7378), "gwalior": (26.2183, 78.1828),
            "mandsaur": (24.0620, 75.0684), "khargone": (21.8155, 75.6080),
            "vidisha": (23.5230, 77.8188), "hoshangabad": (22.7441, 77.7349),
            "default": (23.2599, 77.4126),
        }
        lat, lng = MANDI_COORDS.get(mandi, MANDI_COORDS["default"])
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    f"{settings.OPEN_METEO_BASE_URL}/forecast",
                    params={
                        "latitude": lat, "longitude": lng,
                        "daily": "precipitation_sum,temperature_2m_max,relative_humidity_2m_max,wind_speed_10m_max",
                        "start_date": start_date.strftime("%Y-%m-%d"),
                        "end_date": end_date.strftime("%Y-%m-%d"),
                        "timezone": "Asia/Kolkata",
                    },
                    timeout=10.0,
                )
                if r.status_code != 200:
                    logger.warning(f"Weather API returned {r.status_code}: {r.text[:200]}")
                    return {}
                return r.json().get("daily", {})
        except Exception as e:
            logger.warning(f"Weather fetch failed: {e}. Using defaults.")
            return {}

    def _build_features(self, prices: list, weather: dict, lookback_days: int) -> np.ndarray:
        n = min(len(prices), lookback_days)
        if n < lookback_days:
            pad = lookback_days - n
            pad_price = prices[0].get("modal_price", 2500.0) if prices else 2500.0
            prices = [{"modal_price": pad_price}] * pad + prices

        price_vals = np.array([p.get("modal_price", 2500.0) for p in prices[-lookback_days:]])
        arrival_vals = np.array([p.get("arrival_tonnes", 1200.0) for p in prices[-lookback_days:]])

        rain_vals = np.zeros(lookback_days)
        temp_vals = np.full(lookback_days, 30.0)

        if weather:
            rain_raw = weather.get("precipitation_sum", [])
            temp_raw = weather.get("temperature_2m_max", [])
            rain_vals[:len(rain_raw)] = [v if v is not None else 0 for v in rain_raw[:lookback_days]]
            temp_vals[:len(temp_raw)] = [v if v is not None else 30.0 for v in temp_raw[:lookback_days]]

        features = np.zeros((lookback_days, 13))
        for i in range(lookback_days):
            date_offset = datetime.now() - timedelta(days=lookback_days - i)
            month_angle = 2 * np.pi * date_offset.month / 12
            dow_angle = 2 * np.pi * date_offset.weekday() / 7
            rolling_window = price_vals[max(0, i - 7):i + 1]

            features[i] = [
                price_vals[max(0, i - 1)],
                price_vals[max(0, i - 7)],
                price_vals[max(0, i - 14)],
                price_vals[max(0, i - 30)] if i >= 30 else price_vals[0],
                arrival_vals[i],
                rain_vals[i],
                temp_vals[i],
                np.sin(month_angle),
                np.cos(month_angle),
                np.sin(dow_angle),
                np.cos(dow_angle),
                np.mean(rolling_window),
                np.std(rolling_window) if len(rolling_window) > 1 else 0,
            ]
        return features
