import torch
import numpy as np
import pickle
from ml.models.lstm_attention import LSTMWithAttention
from ml.explainability.shap_explainer import SHAPExplainer
from ml.optimization.decision_engine import DecisionEngine
from backend.schemas.prediction import PredictionResponse, PricePrediction
from backend.schemas.explanation import ExplanationResponse, FeatureImpact
from backend.schemas.recommendation import RecommendationResponse, RecommendationRequest
from backend.services.data_service import DataService
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ModelService:
    def __init__(self):
        self.model = None
        self.X_scaler = None
        self.y_scaler = None
        self.shap_explainer = None
        self.data_service = DataService()
        self.decision_engine = DecisionEngine()
        self.feature_names = [
            "price_lag_1","price_lag_7","price_lag_14","price_lag_30",
            "arrival_volume","rainfall_mm","temperature_max",
            "month_sin","month_cos","day_of_week_sin","day_of_week_cos",
            "price_rolling_7d_mean","price_rolling_7d_std",
        ]
        self.feature_names_hi = {
            "price_lag_1": "कल का भाव",
            "price_lag_7": "7 दिन पहले का भाव",
            "price_lag_14": "14 दिन पहले का भाव",
            "price_lag_30": "1 महीने पहले का भाव",
            "arrival_volume": "आवक (क्विंटल)",
            "rainfall_mm": "बारिश (मिमी)",
            "temperature_max": "अधिकतम तापमान",
            "month_sin": "मौसम (साइन)",
            "month_cos": "मौसम (कोसाइन)",
            "day_of_week_sin": "सप्ताह का दिन",
            "day_of_week_cos": "सप्ताह का दिन (cos)",
            "price_rolling_7d_mean": "7-दिन का औसत भाव",
            "price_rolling_7d_std": "7-दिन का भाव उतार-चढ़ाव",
        }

    def load_model(self, model_path: str):
        """Load trained PyTorch model and scaler from disk."""
        try:
            self.model = LSTMWithAttention(
                input_size=len(self.feature_names),
                hidden_size=128,
                num_layers=2,
                output_size=14,  # 14-day forecast
                dropout=0.2
            )
            self.model.load_state_dict(torch.load(model_path, map_location="cpu"))
            self.model.eval()

            # Note: The prompt uses self.scaler_path which is not defined, defining it conceptually
            scaler_path = model_path.replace("lstm_attention_v1.pt", "scaler.pkl")
            try:
                with open(scaler_path, "rb") as f:
                    scalers = pickle.load(f)
                    if isinstance(scalers, dict) and "X_scaler" in scalers:
                        self.X_scaler = scalers["X_scaler"]
                        self.y_scaler = scalers["y_scaler"]
                    else:
                        logger.warning("Found old format scaler.pkl, skipping.")
            except Exception:
                logger.warning(f"Scaler not found at {scaler_path}")

            # Init SHAP with background data
            background = torch.zeros(50, 30, len(self.feature_names))
            self.shap_explainer = SHAPExplainer(self.model, background)
            logger.info(f"Model loaded from {model_path}")
        except FileNotFoundError:
            logger.warning(f"Model file not found at {model_path}. Using mock predictions.")
            self.model = None
        except Exception as e:
            logger.warning(f"Model load failed: {e}. Using mock predictions.")
            self.model = None

    async def predict(self, crop: str, mandi: str, horizon_days: int) -> PredictionResponse:
        """Generate probabilistic price forecast."""
        # Fetch recent 30 days of data
        features = await self.data_service.get_features(crop, mandi, lookback_days=30)
        
        if self.X_scaler:
            scaled_features = self.X_scaler.transform(features)
        else:
            scaled_features = features
            
        X = torch.tensor(scaled_features, dtype=torch.float32).unsqueeze(0)  # [1, 30, features]

        with torch.no_grad():
            if self.model:
                mean_pred, std_pred = self.model(X)
                means = mean_pred.squeeze().numpy()
                stds  = std_pred.squeeze().numpy()
                
                if self.y_scaler:
                    means = self.y_scaler.inverse_transform(means.reshape(1, -1)).squeeze()
                    stds = stds * self.y_scaler.scale_
                    
                # Fix any negative bounds caused by inverse
                means = np.maximum(means, 0)
                stds = np.maximum(stds, 10)
            else:
                # Mock data for testing without trained model
                base = 2500 + np.random.randn() * 200
                means = base + np.cumsum(np.random.randn(14) * 50)
                stds  = np.abs(np.random.randn(14) * 80 + 120)

        predictions = []
        for i in range(min(horizon_days, 14)):
            predictions.append(PricePrediction(
                date=(datetime.now() + timedelta(days=i+1)).date(),
                predicted_price=round(float(means[i]), 2),
                lower_bound=round(float(means[i] - 1.28 * stds[i]), 2),
                upper_bound=round(float(means[i] + 1.28 * stds[i]), 2),
                confidence=round(float(1 / (1 + stds[i] / (abs(means[i]) + 1))), 3),
            ))

        # Determine trend
        if len(predictions) >= 7:
            trend_val = predictions[-1].predicted_price - predictions[0].predicted_price
            trend = "rising" if trend_val > 50 else ("falling" if trend_val < -50 else "stable")
        else:
            trend = "stable"

        # Risk level based on confidence interval width
        avg_ci_width = np.mean([p.upper_bound - p.lower_bound for p in predictions])
        risk_level = "low" if avg_ci_width < 200 else ("medium" if avg_ci_width < 400 else "high")

        return PredictionResponse(
            crop=crop,
            mandi=mandi,
            predictions=predictions,
            trend=trend,
            risk_level=risk_level,
            generated_at=datetime.utcnow().isoformat(),
        )

    async def explain(self, crop: str, mandi: str, horizon_days: int) -> ExplanationResponse:
        """Generate SHAP-based explanation for prediction."""
        features = await self.data_service.get_features(crop, mandi, lookback_days=30)
        
        if self.X_scaler:
            scaled_features = self.X_scaler.transform(features)
        else:
            scaled_features = features
            
        X = torch.tensor(scaled_features, dtype=torch.float32).unsqueeze(0)

        if self.model and self.shap_explainer:
            shap_vals = self.shap_explainer.compute(X)
            attention_weights = self.model.get_attention_weights(X).tolist()
            current_values = features[-1].tolist() # preserve original unscaled values for display
            
            # Since SHAP outputs feature attributions on the *scaled* output plane, 
            # we must multiply them by the scalar scale to interpret as Rupees.
            if self.y_scaler:
                # We use the scale of the first future day as an approximation for the scalar
                sv_scale = self.y_scaler.scale_[0] 
                shap_vals = shap_vals * sv_scale
        else:
            shap_vals = np.random.randn(len(self.feature_names)) * 50
            attention_weights = list(np.random.dirichlet(np.ones(30)))
            current_values = [2500, 2450, 2300, 2200, 1200, 5.2, 32.1, 0.5, 0.8, 0.7, 0.7, 2400, 120]

        top_indices = np.argsort(np.abs(shap_vals))[-5:][::-1]
        top_drivers = []
        for idx in top_indices:
            name = self.feature_names[idx]
            sv = float(shap_vals[idx])
            top_drivers.append(FeatureImpact(
                feature_name=name,
                feature_name_hi=self.feature_names_hi.get(name, name),
                shap_value=round(sv, 2),
                current_value=round(float(current_values[idx]), 2),
                direction="positive" if sv > 0 else "negative",
                human_explanation=self._generate_explanation(name, sv, current_values[idx]),
                human_explanation_hi=self._generate_explanation_hi(name, sv, current_values[idx]),
            ))

        baseline_price = 2400.0
        predicted_price = baseline_price + float(np.sum(shap_vals))

        return ExplanationResponse(
            prediction_summary=f"Price expected to {'rise' if predicted_price > baseline_price else 'fall'} by ₹{abs(round(predicted_price - baseline_price))} from baseline",
            prediction_summary_hi=f"भाव में {'वृद्धि' if predicted_price > baseline_price else 'कमी'} ₹{abs(round(predicted_price - baseline_price))} की संभावना",
            top_drivers=top_drivers,
            attention_weights=attention_weights,
            baseline_price=round(baseline_price, 2),
            predicted_price=round(predicted_price, 2),
            counterfactuals={
                "store_7d": round(predicted_price * 1.03, 2),
                "store_14d": round(predicted_price * 1.06, 2),
                "sell_now": round(baseline_price, 2),
            }
        )

    async def recommend(self, req: RecommendationRequest) -> RecommendationResponse:
        """Generate sell/store/harvest recommendation."""
        pred = await self.predict(req.crop, req.mandi, horizon_days=14)

        # Fetch current weather for factor analysis
        weather_info = {}
        try:
            weather_raw = await self.data_service._fetch_weather(
                req.mandi,
                __import__('datetime').datetime.now() - __import__('datetime').timedelta(days=3),
                __import__('datetime').datetime.now(),
            )
            rain_vals = weather_raw.get("precipitation_sum", [])
            temp_vals = weather_raw.get("temperature_2m_max", [])
            hum_vals = weather_raw.get("relative_humidity_2m_max", [])
            weather_info = {
                "rainfall": sum(v for v in rain_vals if v is not None) if rain_vals else 0.0,
                "temperature": max((v for v in temp_vals if v is not None), default=30.0) if temp_vals else 30.0,
                "relative_humidity_2m_max": max((v for v in hum_vals if v is not None), default=50.0) if hum_vals else 50.0,
            }
        except Exception:
            weather_info = {"rainfall": 0.0, "temperature": 30.0, "relative_humidity_2m_max": 50.0}

        return self.decision_engine.compute(req, pred, weather_info=weather_info)

    def _generate_explanation(self, feature: str, shap_val: float, current_val: float) -> str:
        direction = "increased" if shap_val > 0 else "decreased"
        templates = {
            "arrival_volume": f"Arrival volume ({current_val:.0f} quintals) has {direction} predicted price by ₹{abs(shap_val):.0f}",
            "rainfall_mm": f"Recent rainfall ({current_val:.1f}mm) has {direction} price by ₹{abs(shap_val):.0f}",
            "temperature_max": f"High temperature ({current_val:.1f}°C) has {direction} price by ₹{abs(shap_val):.0f}",
            "price_lag_7": f"Price trend from last week has {direction} forecast by ₹{abs(shap_val):.0f}",
        }
        return templates.get(feature, f"{feature} has {direction} price by ₹{abs(shap_val):.0f}")

    def _generate_explanation_hi(self, feature: str, shap_val: float, current_val: float) -> str:
        direction = "बढ़ाया" if shap_val > 0 else "घटाया"
        templates = {
            "arrival_volume": f"आवक ({current_val:.0f} क्विंटल) ने भाव ₹{abs(shap_val):.0f} {direction}",
            "rainfall_mm": f"हाल की बारिश ({current_val:.1f}मिमी) ने भाव ₹{abs(shap_val):.0f} {direction}",
        }
        return templates.get(feature, f"इस कारक ने भाव ₹{abs(shap_val):.0f} {direction}")

    async def optimize_harvest(self, crop: str, mandi: str, field_ready_date=None):
        """Generate harvest window optimization using weather + price predictions."""
        from backend.schemas.prediction import PredictionRequest
        
        # Get price predictions for 14 days
        pred = await self.predict(crop, mandi, horizon_days=14)
        
        # Fetch 14-day weather forecast
        weather_raw = {}
        try:
            weather_raw = await self.data_service._fetch_weather(
                mandi,
                datetime.now(),
                datetime.now() + timedelta(days=14),
            )
        except Exception as e:
            logger.warning(f"Weather fetch failed for harvest: {e}")
        
        # Build a mock request object for the decision engine
        req = type('HarvestReq', (), {'crop': crop, 'mandi': mandi})()
        
        return self.decision_engine.compute_harvest_window(req, pred, weather_raw)

