"""Helper utilities for MandiMitra ML module."""
import numpy as np
from datetime import datetime


def format_price(price: float) -> str:
    """Format price in Indian Rupee notation."""
    return f"₹{price:,.2f}"


def date_to_features(dt: datetime) -> dict:
    """Extract cyclical date features from a datetime object."""
    month_angle = 2 * np.pi * dt.month / 12
    dow_angle = 2 * np.pi * dt.weekday() / 7
    return {
        "month_sin": np.sin(month_angle),
        "month_cos": np.cos(month_angle),
        "day_of_week_sin": np.sin(dow_angle),
        "day_of_week_cos": np.cos(dow_angle),
    }


def split_data(X, y, train_ratio=0.8, val_ratio=0.1):
    """Split data into train/val/test sets chronologically."""
    n = len(X)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))

    return {
        "X_train": X[:train_end],
        "y_train": y[:train_end],
        "X_val": X[train_end:val_end],
        "y_val": y[train_end:val_end],
        "X_test": X[val_end:],
        "y_test": y[val_end:],
    }
