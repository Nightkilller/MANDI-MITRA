import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

MANDI_COORDS = {
    "indore":   (22.7196, 75.8577),
    "bhopal":   (23.2599, 77.4126),
    "ujjain":   (23.1765, 75.7885),
    "jabalpur": (23.1815, 79.9864),
    "sagar":    (23.8388, 78.7378),
    "gwalior":  (26.2183, 78.1828),
    "mandsaur": (24.0620, 75.0684),
    "khargone": (21.8155, 75.6080),
    "vidisha":  (23.5230, 77.8188),
    "hoshangabad": (22.7441, 77.7349)
}

def download_historical_weather():
    """
    Downloads historical daily weather data using the official openmeteo-requests client.
    Uses cached sessions to prevent redownloading massive datasets on failure.
    """
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600 * 24) # 24 hr cache
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Use the archive API for historical data
    from datetime import timedelta
    url = "https://archive-api.open-meteo.com/v1/archive"
    end_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    start_date = "2023-01-01"

    # Requested daily agricultural variables
    daily_vars = [
        "temperature_2m_max", 
        "temperature_2m_min", 
        "precipitation_sum", 
        "soil_moisture_0_to_7cm_mean",
        "wind_speed_10m_max"
    ]

    for mandi, (lat, lng) in MANDI_COORDS.items():
        logger.info(f"Fetching historical weather for {mandi} ({lat}, {lng})...")
        
        params = {
            "latitude": lat,
            "longitude": lng,
            "start_date": start_date,
            "end_date": end_date,
            "daily": daily_vars,
            "timezone": "Asia/Kolkata"
        }
        
        try:
            responses = openmeteo.weather_api(url, params=params)
            response = responses[0]
            
            # Process daily data
            daily = response.Daily()
            
            # Extract variables. The order matches the sequence requested in `daily_vars`
            daily_temp_max = daily.Variables(0).ValuesAsNumpy()
            daily_temp_min = daily.Variables(1).ValuesAsNumpy()
            daily_precip = daily.Variables(2).ValuesAsNumpy()
            daily_soil = daily.Variables(3).ValuesAsNumpy()
            daily_wind = daily.Variables(4).ValuesAsNumpy()
            
            # Create a localized time index
            daily_data = {"date": pd.date_range(
                start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
                end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
                freq = pd.Timedelta(seconds = daily.Interval()),
                inclusive = "left"
            )}
            
            # Add variables to dictionary
            daily_data["temperature_2m_max"] = daily_temp_max
            daily_data["temperature_2m_min"] = daily_temp_min
            daily_data["precipitation_sum"] = daily_precip
            daily_data["soil_moisture_mean"] = daily_soil
            daily_data["wind_speed_10m_max"] = daily_wind
            daily_data["mandi"] = mandi
            
            # Build DataFrame and save
            df = pd.DataFrame(data=daily_data)
            df.to_csv(f"data/raw/weather_{mandi}.csv", index=False)
            
            logger.info(f"Successfully saved {len(df)} days of historical data to weather_{mandi}.csv")
            
        except Exception as e:
            logger.error(f"Failed to fetch data for {mandi}: {e}")

if __name__ == "__main__":
    download_historical_weather()
