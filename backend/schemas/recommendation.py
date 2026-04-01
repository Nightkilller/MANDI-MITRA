from pydantic import BaseModel
from typing import List, Optional


class StorageScenario(BaseModel):
    days: int
    expected_price: float
    storage_cost: float
    spoilage_risk_pct: float
    expected_profit: float
    net_vs_sell_now: float


class ReasonFactor(BaseModel):
    icon: str
    title: str
    title_hi: str
    description: str
    description_hi: str
    impact: str  # "positive" | "negative" | "neutral"
    value: Optional[str] = None


class RecommendationRequest(BaseModel):
    crop: str
    mandi: str
    quantity_quintals: float
    storage_available: bool
    harvest_date: str  # ISO date string


class RecommendationResponse(BaseModel):
    action: str  # "SELL_NOW" | "STORE_7D" | "STORE_14D" | "HARVEST_DELAY"
    action_hi: str
    confidence: float
    reasoning: str
    reasoning_hi: str
    sell_now_profit: float
    scenarios: List[StorageScenario]
    optimal_scenario: StorageScenario
    risk_warning: str
    factors: List[ReasonFactor] = []
