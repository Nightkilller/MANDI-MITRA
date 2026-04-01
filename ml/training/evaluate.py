"""
Evaluation metrics for model performance.
Computes MAE, RMSE, MAPE, and calibration scores.
"""
import numpy as np
import torch
from ml.models.lstm_attention import LSTMWithAttention
import logging

logger = logging.getLogger(__name__)


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Error."""
    return float(np.mean(np.abs(y_true - y_pred)))


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Root Mean Squared Error."""
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Percentage Error. Handles zero division."""
    mask = y_true != 0
    if mask.sum() == 0:
        return 0.0
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)


def coverage_80(y_true: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> float:
    """
    Calibration: fraction of true values within the 80% CI.
    Target should be ~80%.
    """
    in_interval = np.logical_and(y_true >= lower, y_true <= upper)
    return float(np.mean(in_interval) * 100)


def evaluate_model(
    model: LSTMWithAttention,
    X_test: np.ndarray,
    y_test: np.ndarray,
) -> dict:
    """
    Full evaluation of a trained model.
    X_test: [N, lookback_days, n_features]
    y_test: [N, forecast_days]
    Returns dict of metrics.
    """
    X_t = torch.tensor(X_test, dtype=torch.float32)

    model.eval()
    with torch.no_grad():
        mean_pred, std_pred = model(X_t)
        means = mean_pred.numpy()
        stds = std_pred.numpy()

    lower = means - 1.28 * stds
    upper = means + 1.28 * stds

    metrics = {
        "mae": mae(y_test, means),
        "rmse": rmse(y_test, means),
        "mape": mape(y_test, means),
        "coverage_80": coverage_80(y_test, lower, upper),
    }

    # Per-horizon metrics
    for h in [1, 7, 14]:
        if h <= means.shape[1]:
            idx = h - 1
            metrics[f"mae_day{h}"] = mae(y_test[:, idx], means[:, idx])
            metrics[f"rmse_day{h}"] = rmse(y_test[:, idx], means[:, idx])

    logger.info("Evaluation Results:")
    for k, v in metrics.items():
        logger.info(f"  {k}: {v:.4f}")

    return metrics
