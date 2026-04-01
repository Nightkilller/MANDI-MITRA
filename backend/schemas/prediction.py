from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class PredictionRequest(BaseModel):
    crop: str = Field(..., example="tomato")
    mandi: str = Field(..., example="indore")
    horizon_days: int = Field(default=14, ge=1, le=28)
    current_price: Optional[float] = None


class PricePrediction(BaseModel):
    date: date
    predicted_price: float
    lower_bound: float  # 10th percentile
    upper_bound: float  # 90th percentile
    confidence: float  # 0-1 confidence score


class PredictionResponse(BaseModel):
    crop: str
    mandi: str
    predictions: List[PricePrediction]
    trend: str  # "rising" | "falling" | "stable"
    risk_level: str  # "low" | "medium" | "high"
    generated_at: str
