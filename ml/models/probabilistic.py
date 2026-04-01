"""
Probabilistic wrapper for uncertainty estimation.
Wraps the LSTM model with MC Dropout for epistemic uncertainty.
"""
import torch
import numpy as np
from ml.models.lstm_attention import LSTMWithAttention
import logging

logger = logging.getLogger(__name__)


class ProbabilisticWrapper:
    """
    Monte Carlo Dropout wrapper for uncertainty estimation.
    Runs multiple forward passes with dropout enabled to estimate
    epistemic (model) uncertainty in addition to aleatoric (data) uncertainty.
    """

    def __init__(self, model: LSTMWithAttention, n_samples: int = 30):
        self.model = model
        self.n_samples = n_samples

    def predict_with_uncertainty(self, X: torch.Tensor) -> dict:
        """
        Run MC Dropout inference.
        Returns dict with keys: mean, std, lower_10, upper_90, epistemic_std, aleatoric_std
        """
        self.model.train()  # Enable dropout

        all_means = []
        all_stds = []

        with torch.no_grad():
            for _ in range(self.n_samples):
                mean, std = self.model(X)
                all_means.append(mean.numpy())
                all_stds.append(std.numpy())

        self.model.eval()  # Restore eval mode

        all_means = np.array(all_means)  # [n_samples, batch, output_size]
        all_stds = np.array(all_stds)

        # Epistemic uncertainty = variance of means across MC samples
        epistemic_std = np.std(all_means, axis=0)

        # Aleatoric uncertainty = mean of predicted stds
        aleatoric_std = np.mean(all_stds, axis=0)

        # Total uncertainty
        total_std = np.sqrt(epistemic_std ** 2 + aleatoric_std ** 2)

        # Final prediction = mean of means
        final_mean = np.mean(all_means, axis=0)

        return {
            "mean": final_mean,
            "std": total_std,
            "lower_10": final_mean - 1.28 * total_std,
            "upper_90": final_mean + 1.28 * total_std,
            "epistemic_std": epistemic_std,
            "aleatoric_std": aleatoric_std,
        }

    def calibration_score(self, X: torch.Tensor, y_true: np.ndarray) -> float:
        """
        Compute calibration: what fraction of true values fall within
        the predicted 80% confidence interval.
        """
        result = self.predict_with_uncertainty(X)
        in_interval = np.logical_and(
            y_true >= result["lower_10"], y_true <= result["upper_90"]
        )
        coverage = np.mean(in_interval)
        logger.info(f"Calibration coverage (target 80%): {coverage * 100:.1f}%")
        return float(coverage)
