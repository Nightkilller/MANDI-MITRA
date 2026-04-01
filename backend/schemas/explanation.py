from pydantic import BaseModel
from typing import List, Dict


class FeatureImpact(BaseModel):
    feature_name: str
    feature_name_hi: str
    shap_value: float
    current_value: float
    direction: str  # "positive" | "negative"
    human_explanation: str
    human_explanation_hi: str


class ExplanationRequest(BaseModel):
    crop: str
    mandi: str
    horizon_days: int = 7


class ExplanationResponse(BaseModel):
    prediction_summary: str
    prediction_summary_hi: str
    top_drivers: List[FeatureImpact]
    attention_weights: List[float]
    baseline_price: float
    predicted_price: float
    counterfactuals: Dict[str, float]
