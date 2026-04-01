"""
XGBoost baseline model for mandi price prediction.
Used as a comparison benchmark against the LSTM + Attention model.
"""
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pickle
import os
import logging

logger = logging.getLogger(__name__)


class XGBoostBaseline:
    """XGBoost baseline model for single-step price prediction."""

    def __init__(self, params: dict = None):
        self.params = params or {
            "objective": "reg:squarederror",
            "max_depth": 6,
            "learning_rate": 0.1,
            "n_estimators": 200,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "min_child_weight": 3,
            "reg_alpha": 0.1,
            "reg_lambda": 1.0,
            "random_state": 42,
        }
        self.model = xgb.XGBRegressor(**self.params)
        self.feature_names = [
            "price_lag_1",
            "price_lag_7",
            "price_lag_14",
            "price_lag_30",
            "arrival_volume",
            "rainfall_mm",
            "temperature_max",
            "month_sin",
            "month_cos",
            "day_of_week_sin",
            "day_of_week_cos",
            "price_rolling_7d_mean",
            "price_rolling_7d_std",
        ]

    def train(self, X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray):
        """
        Train XGBoost model.
        X: [N, n_features] (flattened — no time dimension)
        y: [N] (single step target)
        """
        self.model.fit(
            X_train,
            y_train,
            eval_set=[(X_val, y_val)],
            verbose=10,
        )
        # Validation metrics
        y_pred = self.model.predict(X_val)
        mae = mean_absolute_error(y_val, y_pred)
        rmse = np.sqrt(mean_squared_error(y_val, y_pred))
        logger.info(f"XGBoost Baseline — MAE: {mae:.2f}, RMSE: {rmse:.2f}")
        return {"mae": mae, "rmse": rmse}

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict prices. X: [N, n_features]"""
        return self.model.predict(X)

    def feature_importance(self) -> dict:
        """Return feature importance scores."""
        importances = self.model.feature_importances_
        return dict(zip(self.feature_names, importances.tolist()))

    def save(self, path: str):
        """Save model to disk."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self.model, f)
        logger.info(f"XGBoost model saved to {path}")

    def load(self, path: str):
        """Load model from disk."""
        with open(path, "rb") as f:
            self.model = pickle.load(f)
        logger.info(f"XGBoost model loaded from {path}")
