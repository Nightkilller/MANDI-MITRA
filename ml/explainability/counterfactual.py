"""
Counterfactual analysis engine.
Answers: "What if the farmer stored the crop for N more days?"
"""
import numpy as np
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

STORAGE_COST_PER_QUINTAL_PER_DAY = 2.5  # ₹

CROP_SPOILAGE_RATES = {
    "tomato": 0.015,   # 1.5% per day
    "onion": 0.004,    # 0.4% per day
    "wheat": 0.001,    # 0.1% per day
    "soybean": 0.002,  # 0.2% per day
}


class CounterfactualEngine:
    """
    Generates counterfactual scenarios:
    - What if stored for 7 days?
    - What if stored for 14 days?
    - What if sold at a different mandi?
    """

    def compute_storage_scenarios(
        self,
        crop: str,
        current_price: float,
        predicted_prices: List[float],
        quantity_quintals: float = 10.0,
    ) -> Dict[str, dict]:
        """
        Compute profit/loss for different storage durations.
        predicted_prices: list of prices for days 1..N into the future
        """
        spoilage_rate = CROP_SPOILAGE_RATES.get(crop, 0.005)
        scenarios = {}

        for days in [0, 7, 14, 21]:
            if days == 0:
                profit = current_price * quantity_quintals
                scenarios["sell_now"] = {
                    "days": 0,
                    "price": current_price,
                    "profit": round(profit, 2),
                    "storage_cost": 0,
                    "spoilage_pct": 0,
                    "net_vs_now": 0,
                }
            elif days <= len(predicted_prices):
                future_price = predicted_prices[days - 1]
                storage_cost = STORAGE_COST_PER_QUINTAL_PER_DAY * quantity_quintals * days
                effective_qty = quantity_quintals * (1 - spoilage_rate * days)
                profit = future_price * effective_qty - storage_cost
                sell_now_profit = current_price * quantity_quintals

                scenarios[f"store_{days}d"] = {
                    "days": days,
                    "price": round(future_price, 2),
                    "profit": round(profit, 2),
                    "storage_cost": round(storage_cost, 2),
                    "spoilage_pct": round(spoilage_rate * days * 100, 2),
                    "net_vs_now": round(profit - sell_now_profit, 2),
                }

        return scenarios

    def optimal_action(self, scenarios: Dict[str, dict]) -> str:
        """Return the key of the scenario with highest profit."""
        if not scenarios:
            return "sell_now"
        return max(scenarios, key=lambda k: scenarios[k]["profit"])
