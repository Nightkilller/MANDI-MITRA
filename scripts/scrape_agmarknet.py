import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AGMARKNET_BASE = "https://agmarknet.gov.in/SearchCommodityWise.aspx"
STATE_CODE   = "MP"
COMMODITY_CODES = {
    "tomato": "78",
    "onion":  "23",
    "wheat":  "52",
    "soybean":"263",
}

def scrape_mp_prices(crop: str, start_date: str, end_date: str) -> pd.DataFrame:
    commodity_code = COMMODITY_CODES.get(crop)
    if not commodity_code:
        raise ValueError(f"Unknown crop: {crop}")

    all_records = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    while current_date <= end:
        date_str = current_date.strftime("%d-%b-%Y")
        try:
            params = {
                "Tx_Commodity": commodity_code,
                "Tx_State": STATE_CODE,
                "Tx_District": "0",
                "Tx_Market": "0",
                "DateFrom": date_str,
                "DateTo": date_str,
                "Fr_Date": date_str,
                "To_Date": date_str,
                "Tx_Trend": "0",
                "Tx_CommodityHead": crop.capitalize(),
                "Tx_StateHead": "Madhya Pradesh",
                "Tx_DistrictHead": "--Select--",
                "Tx_MarketHead": "--Select--",
            }
            response = requests.get(AGMARKNET_BASE, params=params, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find("table", {"class": "tableagmark_new"})
            if table:
                rows = table.find_all("tr")[1:]
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 8:
                        all_records.append({
                            "date": current_date.strftime("%Y-%m-%d"),
                            "mandi": cols[2].text.strip().lower().replace(" ", "_"),
                            "crop": crop,
                            "variety": cols[3].text.strip(),
                            "min_price": float(cols[5].text.strip() or 0),
                            "max_price": float(cols[6].text.strip() or 0),
                            "modal_price": float(cols[7].text.strip() or 0),
                        })
            time.sleep(0.5)
        except Exception as e:
            logger.warning(f"Failed to scrape {date_str}: {e}")
        current_date += timedelta(days=1)

    df = pd.DataFrame(all_records)
    return df

if __name__ == "__main__":
    logger.info("Starting historical scraper...")
    df = scrape_mp_prices("tomato", "2024-01-01", "2024-01-05")
    print(df.head())
    df.to_csv("data/raw/historical_scrape.csv", index=False)
