"""
Open-Meteo API client for weather data.
Completely free, no API key required.
"""
import httpx
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

OPEN_METEO_BASE = "https://api.open-meteo.com/v1"

MANDI_COORDS = {
    "indore": (22.7196, 75.8577),
    "bhopal": (23.2599, 77.4126),
    "ujjain": (23.1765, 75.7885),
    "jabalpur": (23.1815, 79.9864),
    "sagar": (23.8388, 78.7378),
    "ratlam": (23.3315, 75.0367),
    "dewas": (22.9623, 76.0511),
    "khandwa": (21.8255, 76.3517),
}


async def fetch_weather_async(
    mandi: str, start_date: str, end_date: str
) -> pd.DataFrame:
    """
    Fetch daily weather data from Open-Meteo (async).
    Returns DataFrame with columns: date, rainfall_mm, temp_max, temp_min, humidity
    """
    lat, lng = MANDI_COORDS.get(mandi, MANDI_COORDS["bhopal"])

    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{OPEN_METEO_BASE}/forecast",
                params={
                    "latitude": lat,
                    "longitude": lng,
                    "daily": "precipitation_sum,temperature_2m_max,temperature_2m_min,relative_humidity_2m_mean",
                    "start_date": start_date,
                    "end_date": end_date,
                    "timezone": "Asia/Kolkata",
                },
                timeout=10.0,
            )
            data = r.json()
            daily = data.get("daily", {})

            df = pd.DataFrame(
                {
                    "date": daily.get("time", []),
                    "rainfall_mm": daily.get("precipitation_sum", []),
                    "temp_max": daily.get("temperature_2m_max", []),
                    "temp_min": daily.get("temperature_2m_min", []),
                    "humidity": daily.get("relative_humidity_2m_mean", []),
                }
            )
            df["mandi"] = mandi
            return df

    except Exception as e:
        logger.warning(f"Weather fetch failed for {mandi}: {e}")
        return pd.DataFrame()


def fetch_weather_sync(
    mandi: str, start_date: str, end_date: str
) -> pd.DataFrame:
    """Synchronous version for scripts and notebooks."""
    import requests

    lat, lng = MANDI_COORDS.get(mandi, MANDI_COORDS["bhopal"])

    try:
        r = requests.get(
            f"{OPEN_METEO_BASE}/forecast",
            params={
                "latitude": lat,
                "longitude": lng,
                "daily": "precipitation_sum,temperature_2m_max,temperature_2m_min",
                "start_date": start_date,
                "end_date": end_date,
                "timezone": "Asia/Kolkata",
            },
            timeout=10,
        )
        data = r.json()
        daily = data.get("daily", {})

        df = pd.DataFrame(
            {
                "date": daily.get("time", []),
                "rainfall_mm": daily.get("precipitation_sum", []),
                "temp_max": daily.get("temperature_2m_max", []),
                "temp_min": daily.get("temperature_2m_min", []),
            }
        )
        df["mandi"] = mandi
        return df

    except Exception as e:
        logger.warning(f"Weather fetch failed for {mandi}: {e}")
        return pd.DataFrame()
