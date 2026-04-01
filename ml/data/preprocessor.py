"""
Feature engineering pipeline.
Transforms raw price + weather data into model-ready features.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle
import os
import logging

logger = logging.getLogger(__name__)


class FeaturePreprocessor:
    """Build feature matrix from raw price and weather data."""

    FEATURE_NAMES = [
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

    def __init__(self):
        self.scaler = StandardScaler()
        self.is_fitted = False

    def build_features(
        self,
        prices_df: pd.DataFrame,
        weather_df: pd.DataFrame = None,
    ) -> pd.DataFrame:
        """
        Build feature columns from raw data.
        prices_df must have: date, modal_price, arrival_tonnes (optional)
        weather_df must have: date, rainfall_mm, temp_max (optional)
        """
        df = prices_df.copy()
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)

        # Price lags
        df["price_lag_1"] = df["modal_price"].shift(1)
        df["price_lag_7"] = df["modal_price"].shift(7)
        df["price_lag_14"] = df["modal_price"].shift(14)
        df["price_lag_30"] = df["modal_price"].shift(30)

        # Arrival volume (use column if available, else placeholder)
        if "arrival_tonnes" in df.columns:
            df["arrival_volume"] = df["arrival_tonnes"]
        else:
            df["arrival_volume"] = 1200.0

        # Weather features
        if weather_df is not None and not weather_df.empty:
            weather_df["date"] = pd.to_datetime(weather_df["date"])
            df = df.merge(weather_df[["date", "rainfall_mm", "temp_max"]], on="date", how="left")
        if "rainfall_mm" not in df.columns:
            df["rainfall_mm"] = 0.0
        if "temp_max" not in df.columns:
            df["temperature_max"] = 30.0
        else:
            df["temperature_max"] = df["temp_max"]

        # Cyclical time features
        df["month_sin"] = np.sin(2 * np.pi * df["date"].dt.month / 12)
        df["month_cos"] = np.cos(2 * np.pi * df["date"].dt.month / 12)
        df["day_of_week_sin"] = np.sin(2 * np.pi * df["date"].dt.dayofweek / 7)
        df["day_of_week_cos"] = np.cos(2 * np.pi * df["date"].dt.dayofweek / 7)

        # Rolling statistics
        df["price_rolling_7d_mean"] = df["modal_price"].rolling(7, min_periods=1).mean()
        df["price_rolling_7d_std"] = df["modal_price"].rolling(7, min_periods=1).std().fillna(0)

        # Fill NaN from lags
        df = df.fillna(method="bfill").fillna(method="ffill").fillna(0)

        return df[self.FEATURE_NAMES + ["date", "modal_price"]]

    def create_sequences(
        self,
        features_df: pd.DataFrame,
        lookback: int = 30,
        forecast: int = 14,
    ) -> tuple:
        """
        Create sliding window sequences for LSTM training.
        Returns: X [N, lookback, n_features], y [N, forecast]
        """
        feature_cols = self.FEATURE_NAMES
        data = features_df[feature_cols].values
        prices = features_df["modal_price"].values

        X, y = [], []
        for i in range(lookback, len(data) - forecast + 1):
            X.append(data[i - lookback : i])
            y.append(prices[i : i + forecast])

        return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)

    def fit_scaler(self, X: np.ndarray) -> np.ndarray:
        """Fit scaler on training data and transform."""
        n, seq, feat = X.shape
        X_flat = X.reshape(-1, feat)
        X_scaled = self.scaler.fit_transform(X_flat)
        self.is_fitted = True
        return X_scaled.reshape(n, seq, feat)

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Transform using fitted scaler."""
        if not self.is_fitted:
            raise ValueError("Scaler not fitted. Call fit_scaler first.")
        n, seq, feat = X.shape
        X_flat = X.reshape(-1, feat)
        X_scaled = self.scaler.transform(X_flat)
        return X_scaled.reshape(n, seq, feat)

    def save_scaler(self, path: str):
        """Save fitted scaler to disk."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self.scaler, f)
        logger.info(f"Scaler saved to {path}")

    def load_scaler(self, path: str):
        """Load scaler from disk."""
        with open(path, "rb") as f:
            self.scaler = pickle.load(f)
        self.is_fitted = True
        logger.info(f"Scaler loaded from {path}")
