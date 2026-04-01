import numpy as np
import logging

logger = logging.getLogger(__name__)

STORAGE_COST_PER_QUINTAL_PER_DAY = 2.5  # ₹ per quintal per day
SPOILAGE_BASE_RATE = 0.005  # 0.5% per day base spoilage

CROP_SPOILAGE = {
    "tomato": 0.015,   # 1.5% per day — highly perishable
    "onion": 0.004,    # 0.4% per day
    "wheat": 0.001,    # 0.1% per day — very stable
    "soybean": 0.002,  # 0.2% per day
    "garlic": 0.003,   # 0.3% per day
    "potato": 0.006,   # 0.6% per day
    "mustard": 0.001,  # 0.1% per day
    "gram": 0.0015,    # 0.15% per day
    "maize": 0.0015,   # 0.15% per day
    "cotton": 0.001    # 0.1% per day
}

CROP_NAMES_HI = {
    "tomato": "टमाटर",
    "onion": "प्याज",
    "wheat": "गेहूं",
    "soybean": "सोयाबीन",
    "garlic": "लहसुन",
    "potato": "आलू",
    "mustard": "सरसों",
    "gram": "चना",
    "maize": "मक्का",
    "cotton": "कपास",
}


class DecisionEngine:
    def compute(self, req, pred, weather_info=None) -> "RecommendationResponse":
        from backend.schemas.recommendation import (
            RecommendationResponse,
            StorageScenario,
            ReasonFactor,
        )

        crop = req.crop
        qty = req.quantity_quintals
        spoilage_rate = CROP_SPOILAGE.get(crop, SPOILAGE_BASE_RATE)

        # Current market price (day 0 prediction)
        current_price = (
            pred.predictions[0].predicted_price if pred.predictions else 2500.0
        )
        sell_now_profit = round(current_price * qty, 2)

        scenarios = []
        storage_days_options = [7, 14] if req.storage_available else []

        for days in storage_days_options:
            future_pred = next(
                (
                    p
                    for p in pred.predictions
                    if (p.date - pred.predictions[0].date).days >= days - 1
                ),
                pred.predictions[-1],
            )
            future_price = future_pred.predicted_price

            spoilage_loss_pct = spoilage_rate * days * 100
            effective_qty = qty * (1 - spoilage_rate * days)
            storage_cost = STORAGE_COST_PER_QUINTAL_PER_DAY * qty * days
            expected_profit = round(future_price * effective_qty - storage_cost, 2)
            net_vs_now = round(expected_profit - sell_now_profit, 2)

            scenarios.append(
                StorageScenario(
                    days=days,
                    expected_price=round(future_price, 2),
                    storage_cost=round(storage_cost, 2),
                    spoilage_risk_pct=round(spoilage_loss_pct, 2),
                    expected_profit=expected_profit,
                    net_vs_sell_now=net_vs_now,
                )
            )

        # Pick best action
        if not scenarios:
            best_action = "SELL_NOW"
            optimal = StorageScenario(
                days=0,
                expected_price=current_price,
                storage_cost=0,
                spoilage_risk_pct=0,
                expected_profit=sell_now_profit,
                net_vs_sell_now=0,
            )
        else:
            best_scenario = max(scenarios, key=lambda s: s.expected_profit)
            optimal = best_scenario
            if best_scenario.net_vs_sell_now > 200:
                best_action = f"STORE_{best_scenario.days}D"
            else:
                best_action = "SELL_NOW"
                optimal = StorageScenario(
                    days=0,
                    expected_price=current_price,
                    storage_cost=0,
                    spoilage_risk_pct=0,
                    expected_profit=sell_now_profit,
                    net_vs_sell_now=0,
                )

        # Risk warning
        risk_warning = ""
        if pred.risk_level == "high":
            risk_warning = (
                "High price volatility detected. Prediction confidence is low."
            )
        if crop == "tomato" and best_action != "SELL_NOW":
            risk_warning += (
                " Tomato is highly perishable — storage risk is significant."
            )

        reasoning_map = {
            "SELL_NOW": (
                "Current prices are optimal or storage costs outweigh future gains.",
                "अभी बेचना सबसे फायदेमंद है। भंडारण लागत भविष्य के लाभ से अधिक है।",
            ),
            "STORE_7D": (
                f"Prices expected to rise ₹{abs(optimal.net_vs_sell_now):.0f} in 7 days, offsetting storage cost.",
                f"7 दिनों में भाव ₹{abs(optimal.net_vs_sell_now):.0f} बढ़ने की संभावना।",
            ),
            "STORE_14D": (
                f"Prices expected to rise significantly in 14 days (net gain ₹{abs(optimal.net_vs_sell_now):.0f}).",
                f"14 दिनों में भाव में अच्छी वृद्धि संभव (लाभ ₹{abs(optimal.net_vs_sell_now):.0f})।",
            ),
        }
        reasoning_en, reasoning_hi = reasoning_map.get(
            best_action, ("Insufficient data.", "पर्याप्त डेटा नहीं।")
        )

        # Generate detailed reasoning factors
        factors = self._generate_factors(
            crop, pred, current_price, optimal, best_action, weather_info
        )

        return RecommendationResponse(
            action=best_action,
            action_hi={
                "SELL_NOW": "अभी बेचें",
                "STORE_7D": "7 दिन रखें",
                "STORE_14D": "14 दिन रखें",
            }.get(best_action, best_action),
            confidence=(
                round(
                    float(1.0 - pred.predictions[0].predicted_price / 5000), 2
                )
                if pred.predictions
                else 0.5
            ),
            reasoning=reasoning_en,
            reasoning_hi=reasoning_hi,
            sell_now_profit=sell_now_profit,
            scenarios=scenarios,
            optimal_scenario=optimal,
            risk_warning=risk_warning,
            factors=factors,
        )

    def _generate_factors(self, crop, pred, current_price, optimal, action, weather_info):
        from backend.schemas.recommendation import ReasonFactor

        factors = []
        crop_hi = CROP_NAMES_HI.get(crop, crop)
        spoilage_rate = CROP_SPOILAGE.get(crop, SPOILAGE_BASE_RATE)

        # 1. Price Trend Factor
        if len(pred.predictions) >= 7:
            price_7d = pred.predictions[6].predicted_price
            price_change = price_7d - current_price
            pct_change = (price_change / current_price) * 100

            if price_change > 50:
                factors.append(ReasonFactor(
                    icon="📈",
                    title="Price Trend: Rising",
                    title_hi="भाव का रुझान: बढ़ रहा है",
                    description=f"Prices expected to rise by ₹{abs(price_change):.0f} ({pct_change:+.1f}%) over 7 days. Storing could increase your profit.",
                    description_hi=f"7 दिनों में भाव ₹{abs(price_change):.0f} ({pct_change:+.1f}%) बढ़ने की संभावना। भंडारण से लाभ बढ़ सकता है।",
                    impact="positive",
                    value=f"₹{price_change:+.0f}",
                ))
            elif price_change < -50:
                factors.append(ReasonFactor(
                    icon="📉",
                    title="Price Trend: Falling",
                    title_hi="भाव का रुझान: गिर रहा है",
                    description=f"Prices expected to drop by ₹{abs(price_change):.0f} ({pct_change:+.1f}%) over 7 days. Selling now is recommended.",
                    description_hi=f"7 दिनों में भाव ₹{abs(price_change):.0f} ({pct_change:+.1f}%) गिरने की संभावना। अभी बेचना उचित है।",
                    impact="negative",
                    value=f"₹{price_change:+.0f}",
                ))
            else:
                factors.append(ReasonFactor(
                    icon="➡️",
                    title="Price Trend: Stable",
                    title_hi="भाव का रुझान: स्थिर",
                    description=f"Prices expected to remain stable (±₹{abs(price_change):.0f}). Storage may not provide significant gains.",
                    description_hi=f"भाव स्थिर रहने की संभावना (±₹{abs(price_change):.0f})। भंडारण से ज़्यादा लाभ नहीं।",
                    impact="neutral",
                    value=f"₹{price_change:+.0f}",
                ))

        # 2. Weather Factor
        rainfall = 0.0
        temperature = 30.0
        if weather_info:
            rainfall = weather_info.get("rainfall", 0.0)
            temperature = weather_info.get("temperature", 30.0)

        if rainfall > 20:
            factors.append(ReasonFactor(
                icon="🌧️",
                title="Heavy Rainfall Expected",
                title_hi="भारी बारिश की संभावना",
                description=f"Rainfall of {rainfall:.1f}mm expected. This can disrupt supply chains and increase prices, but also risks crop damage during storage.",
                description_hi=f"{rainfall:.1f}mm बारिश की संभावना। यह आपूर्ति श्रृंखला को बाधित कर सकता है और भाव बढ़ा सकता है।",
                impact="positive" if action != "SELL_NOW" else "neutral",
                value=f"{rainfall:.1f}mm",
            ))
        elif rainfall > 5:
            factors.append(ReasonFactor(
                icon="🌦️",
                title="Moderate Rainfall Expected",
                title_hi="मध्यम बारिश की संभावना",
                description=f"Light to moderate rainfall ({rainfall:.1f}mm) expected. Normal market conditions likely.",
                description_hi=f"हल्की से मध्यम बारिश ({rainfall:.1f}mm) की संभावना। बाजार सामान्य रहेगा।",
                impact="neutral",
                value=f"{rainfall:.1f}mm",
            ))
        else:
            factors.append(ReasonFactor(
                icon="☀️",
                title="Dry Weather Forecast",
                title_hi="शुष्क मौसम का अनुमान",
                description=f"No significant rainfall expected ({rainfall:.1f}mm). Good conditions for storage if needed.",
                description_hi=f"कोई विशेष बारिश नहीं ({rainfall:.1f}mm)। भंडारण के लिए अच्छी स्थिति।",
                impact="positive" if action != "SELL_NOW" else "neutral",
                value=f"{rainfall:.1f}mm",
            ))

        # 3. Temperature Factor
        if temperature > 38:
            factors.append(ReasonFactor(
                icon="🌡️",
                title="High Temperature Alert",
                title_hi="उच्च तापमान चेतावनी",
                description=f"Temperature at {temperature:.1f}°C. Perishable crops may spoil faster in storage.",
                description_hi=f"तापमान {temperature:.1f}°C। फसलें भंडारण में जल्दी खराब हो सकती हैं।",
                impact="negative" if crop in ["tomato", "onion", "garlic", "potato"] else "neutral",
                value=f"{temperature:.1f}°C",
            ))
        else:
            factors.append(ReasonFactor(
                icon="🌡️",
                title=f"Temperature: {temperature:.0f}°C",
                title_hi=f"तापमान: {temperature:.0f}°C",
                description=f"Current temperature is {temperature:.1f}°C — within safe range for storage.",
                description_hi=f"वर्तमान तापमान {temperature:.1f}°C — भंडारण के लिए सुरक्षित सीमा में।",
                impact="positive",
                value=f"{temperature:.1f}°C",
            ))

        # 4. Spoilage Risk Factor (Enhanced with Humidity)
        if weather_info is None:
            weather_info = {}
        humidity = weather_info.get("relative_humidity_2m_max", 50.0)
        spoilage_multiplier = 1.0
        
        if temperature > 30 and humidity > 70:
            spoilage_multiplier = 2.0  # Massive penalty for storing in humid heat
            
        adjusted_rate = spoilage_rate * spoilage_multiplier
        spoilage_daily_pct = adjusted_rate * 100
        
        if spoilage_multiplier > 1.0 and crop in ["tomato", "onion", "potato", "garlic"]:
            factors.append(ReasonFactor(
                icon="⚠️",
                title="Extreme Spoilage Risk (Heat+Humid)",
                title_hi="खराब होने का अत्यधिक जोखिम",
                description=f"{crop.capitalize()} is highly perishable under {humidity:.0f}% humidity and {temperature:.0f}°C heat. Spoilage doubled to ~{spoilage_daily_pct:.1f}%/day.",
                description_hi=f"{humidity:.0f}% आर्द्रता और {temperature:.0f}°C गर्मी के कारण {crop_hi} तेजी से खराब होगा।",
                impact="negative",
                value=f"{spoilage_daily_pct:.1f}%/day",
            ))
        elif adjusted_rate >= 0.01:
            factors.append(ReasonFactor(
                icon="⚠️",
                title=f"High Spoilage Risk ({crop_hi})",
                title_hi=f"उच्च खराबी जोखिम ({crop_hi})",
                description=f"{crop.capitalize()} loses ~{spoilage_daily_pct:.1f}% per day in storage. Over 7 days that's {spoilage_daily_pct*7:.1f}% loss. Quick sale is preferred.",
                description_hi=f"{crop_hi} भंडारण में प्रतिदिन ~{spoilage_daily_pct:.1f}% खराब होता है। 7 दिनों में {spoilage_daily_pct*7:.1f}% नुकसान। जल्दी बिक्री बेहतर।",
                impact="negative",
                value=f"{spoilage_daily_pct:.1f}%/day",
            ))
        else:
            factors.append(ReasonFactor(
                icon="✅",
                title=f"Low Spoilage Risk ({crop_hi})",
                title_hi=f"कम खराबी जोखिम ({crop_hi})",
                description=f"{crop.capitalize()} has low spoilage ({spoilage_daily_pct:.1f}%/day). Can be stored safely for 7–14 days.",
                description_hi=f"{crop_hi} में कम खराबी ({spoilage_daily_pct:.1f}%/दिन)। 7-14 दिन सुरक्षित भंडारण संभव।",
                impact="positive",
                value=f"{spoilage_daily_pct:.1f}%/day",
            ))

        # 5. Market Volatility Factor
        if pred.risk_level == "high":
            factors.append(ReasonFactor(
                icon="⚡",
                title="High Market Volatility",
                title_hi="उच्च बाजार अस्थिरता",
                description="Price predictions have wide confidence intervals. Market is unpredictable — consider selling to reduce risk.",
                description_hi="भाव अनुमान में अधिक अनिश्चितता। बाजार अप्रत्याशित — जोखिम कम करने के लिए बिक्री पर विचार करें।",
                impact="negative",
                value=pred.risk_level,
            ))
        elif pred.risk_level == "medium":
            factors.append(ReasonFactor(
                icon="📊",
                title="Moderate Market Stability",
                title_hi="मध्यम बाजार स्थिरता",
                description="Market shows moderate volatility. Predictions have reasonable confidence.",
                description_hi="बाजार में मध्यम उतार-चढ़ाव। अनुमान में उचित विश्वास।",
                impact="neutral",
                value=pred.risk_level,
            ))
        else:
            factors.append(ReasonFactor(
                icon="🛡️",
                title="Stable Market Conditions",
                title_hi="स्थिर बाजार स्थिति",
                description="Market is stable with tight confidence intervals. Predictions are reliable.",
                description_hi="बाजार स्थिर है। अनुमान विश्वसनीय हैं।",
                impact="positive",
                value=pred.risk_level,
            ))

        # 6. Storage Cost Factor
        if action != "SELL_NOW" and optimal.days > 0:
            factors.append(ReasonFactor(
                icon="🏪",
                title=f"Storage Cost: ₹{optimal.storage_cost:.0f}",
                title_hi=f"भंडारण लागत: ₹{optimal.storage_cost:.0f}",
                description=f"Storing for {optimal.days} days costs ₹{STORAGE_COST_PER_QUINTAL_PER_DAY}/quintal/day. Total: ₹{optimal.storage_cost:.0f}. This is factored into the profit calculation.",
                description_hi=f"{optimal.days} दिन भंडारण की लागत ₹{STORAGE_COST_PER_QUINTAL_PER_DAY}/क्विंटल/दिन। कुल: ₹{optimal.storage_cost:.0f}।",
                impact="negative",
                value=f"₹{optimal.storage_cost:.0f}",
            ))

        return factors

    def compute_harvest_window(self, req, pred, weather_raw) -> "HarvestResponse":
        from backend.schemas.harvest import HarvestResponse, HarvestWindow
        import datetime
        
        crop = req.crop
        mandi = req.mandi
        crop_hi = CROP_NAMES_HI.get(crop, crop)

        windows = []
        best_window = None
        max_score = -float('inf')

        # Dummy weather integration for demonstration if open-meteo fails
        precipitation = weather_raw.get("precipitation_sum", [0] * 14)
        temp_max = weather_raw.get("temperature_2m_max", [30] * 14)
        soil_moisture = weather_raw.get("soil_moisture_0_to_7cm", [0.2] * 14)
        relative_humidity = weather_raw.get("relative_humidity_2m_max", [50] * 14)
        wind_speed = weather_raw.get("wind_speed_10m_max", [10] * 14)

        for i, p in enumerate(pred.predictions):
            if i >= 14: break
            
            rain = precipitation[i] if i < len(precipitation) and precipitation[i] is not None else 0.0
            temp = temp_max[i] if i < len(temp_max) and temp_max[i] is not None else 30.0
            soil = soil_moisture[i] if i < len(soil_moisture) and soil_moisture[i] is not None else 0.2
            hum = relative_humidity[i] if i < len(relative_humidity) and relative_humidity[i] is not None else 50.0
            wind = wind_speed[i] if i < len(wind_speed) and wind_speed[i] is not None else 10.0
            
            # Constraints and scoring
            weather_score = 1.0
            if rain > 10: weather_score *= 0.2
            elif rain > 0: weather_score *= 0.8
            
            if soil > 0.4: weather_score *= 0.3 # Muddy tracking penalty
            if wind > 40: weather_score *= 0.5  # High wind lodging penalty
            
            # Simplified yield factor - wait longer = slightly more yield but caps out
            yield_factor = min(1.0, 0.9 + i * 0.015)
            
            # Simple revenue score = Yield * Expected Price * Weather probability
            revenue_score = p.predicted_price * yield_factor * weather_score
            
            window = HarvestWindow(
                day=i,
                date=p.date.isoformat(),
                expected_price=round(p.predicted_price, 2),
                weather_score=round(weather_score, 2),
                yield_factor=round(yield_factor, 2),
                revenue_score=round(revenue_score, 2),
                rainfall_mm=round(rain, 1),
                temperature=round(temp, 1),
                humidity=round(hum, 1),
                wind_speed=round(wind, 1),
                soil_moisture=round(soil, 3),
                is_optimal=False
            )
            windows.append(window)
            
            if revenue_score > max_score:
                max_score = revenue_score
                best_window = window

        for w in windows:
            if w.day == best_window.day:
                w.is_optimal = True

        return HarvestResponse(
            crop=crop,
            mandi=mandi,
            optimal_window=best_window,
            windows=windows,
            recommendation=f"Harvest in {best_window.day} days.",
            recommendation_hi=f"{best_window.day} दिनों में कटाई करें।",
            weather_summary=f"Optimal conditions on {best_window.date} with {best_window.rainfall_mm}mm rain expected.",
            weather_summary_hi=f"{best_window.date} को कटाई के लिए उत्तम मौसम।",
            yield_insight=f"Waiting will optimize yield to {best_window.yield_factor*100:.0f}% potential.",
            yield_insight_hi=f"अपेक्षित उपज क्षमता {best_window.yield_factor*100:.0f}% होगी।"
        )
