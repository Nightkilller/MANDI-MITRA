"""
Attention weight extractor and visualizer.
Extracts temporal attention weights from the LSTM model
to show which past days most influenced the prediction.
"""
import torch
import numpy as np
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class AttentionVisualizer:
    """Extract and format attention weights for frontend visualization."""

    def __init__(self, model):
        self.model = model

    def extract_weights(self, X: torch.Tensor) -> np.ndarray:
        """
        Extract attention weights for a single input sequence.
        X: [1, seq_len, n_features]
        Returns: [seq_len] array of attention weights (sum to 1)
        """
        self.model.eval()
        with torch.no_grad():
            self.model(X)
            weights = self.model._attention_weights
        if weights is None:
            logger.warning("No attention weights found. Returning uniform.")
            seq_len = X.shape[1]
            return np.ones(seq_len) / seq_len
        return weights.squeeze(0).numpy()

    def get_top_attended_days(
        self, weights: np.ndarray, top_k: int = 5
    ) -> List[Tuple[int, float]]:
        """
        Return top-K most attended days (0-indexed from most recent).
        Returns list of (day_index, weight) tuples.
        """
        indices = np.argsort(weights)[-top_k:][::-1]
        return [(int(idx), float(weights[idx])) for idx in indices]

    def format_for_heatmap(
        self, weights: np.ndarray, lookback_days: int = 30
    ) -> List[dict]:
        """
        Format weights for frontend heatmap rendering.
        Returns list of {day: int, weight: float, label: str}.
        """
        result = []
        for i, w in enumerate(weights[-lookback_days:]):
            day_offset = lookback_days - i
            result.append(
                {
                    "day": i,
                    "days_ago": day_offset,
                    "weight": round(float(w), 4),
                    "label": f"{day_offset}d ago",
                }
            )
        return result
