import shap
import torch
import numpy as np
import logging

logger = logging.getLogger(__name__)


class SHAPExplainer:
    """Wrapper around SHAP DeepExplainer for LSTM models."""

    def __init__(self, model, background_data: torch.Tensor):
        self.model = model

        class ModelWrapper(torch.nn.Module):
            def __init__(self, m):
                super().__init__()
                self.m = m
            def forward(self, x):
                mean, _ = self.m(x)
                return mean[:, 0:1]  # Explain first forecast step

        self.explainer = shap.GradientExplainer(ModelWrapper(model), background_data)

    def compute(self, X: torch.Tensor) -> np.ndarray:
        """Returns SHAP values. Shape: [n_features] (averaged over time steps)."""
        try:
            shap_values = self.explainer.shap_values(X)
            # Average over time dimension -> [n_features]
            if isinstance(shap_values, list):
                s = shap_values[0]
            else:
                s = shap_values
            # s has shape [batch, seq, feature, 1]
            return np.mean(np.abs(s[0, :, :, 0]), axis=0)
        except Exception as e:
            logger.warning(f"SHAP computation failed: {e}. Returning zeros.")
            return np.zeros(X.shape[-1])

    def compute_detailed(self, X: torch.Tensor) -> np.ndarray:
        """Returns full SHAP values matrix. Shape: [seq_len, n_features]."""
        try:
            shap_values = self.explainer.shap_values(X, check_additivity=False)
            return shap_values[0]  # [seq_len, n_features]
        except Exception as e:
            logger.warning(f"Detailed SHAP computation failed: {e}")
            return np.zeros((X.shape[1], X.shape[2]))
