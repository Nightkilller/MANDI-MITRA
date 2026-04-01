from pydantic import BaseModel
from typing import List, Optional


class HarvestWindow(BaseModel):
    day: int
    date: str
    expected_price: float
    weather_score: float  # 0-1 (1 = ideal harvest weather)
    yield_factor: float   # 0-1 (1 = peak yield)
    revenue_score: float  # composite score
    rainfall_mm: float
    temperature: float
    humidity: float
    wind_speed: float
    soil_moisture: float
    is_optimal: bool = False


class HarvestRequest(BaseModel):
    crop: str
    mandi: str
    field_ready_date: Optional[str] = None  # ISO date, defaults to today


class HarvestResponse(BaseModel):
    crop: str
    mandi: str
    optimal_window: HarvestWindow
    windows: List[HarvestWindow]
    recommendation: str
    recommendation_hi: str
    weather_summary: str
    weather_summary_hi: str
    yield_insight: str
    yield_insight_hi: str
