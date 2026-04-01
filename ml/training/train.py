import torch
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import os
import logging
from ml.models.lstm_attention import LSTMWithAttention, gaussian_nll_loss
from ml.training.config import TrainingConfig

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def train(config: TrainingConfig, X_train, y_train, X_val, y_val):
    """
    Main training loop.
    X: [N, lookback_days, n_features]  y: [N, forecast_days]
    """
    X_t = torch.tensor(X_train, dtype=torch.float32)
    y_t = torch.tensor(y_train, dtype=torch.float32)
    X_v = torch.tensor(X_val, dtype=torch.float32)
    y_v = torch.tensor(y_val, dtype=torch.float32)

    train_ds = TensorDataset(X_t, y_t)
    train_dl = DataLoader(train_ds, batch_size=config.batch_size, shuffle=True)

    model = LSTMWithAttention(
        input_size=config.input_size,
        hidden_size=config.hidden_size,
        num_layers=config.num_layers,
        output_size=config.output_size,
        dropout=config.dropout,
    )

    optimizer = optim.Adam(
        model.parameters(), lr=config.learning_rate, weight_decay=config.weight_decay
    )
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5, factor=0.5)

    best_val_loss = float("inf")
    patience_counter = 0

    for epoch in range(config.epochs):
        model.train()
        train_losses = []
        for Xb, yb in train_dl:
            optimizer.zero_grad()
            mean, std = model(Xb)
            loss = gaussian_nll_loss(mean, std, yb)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            train_losses.append(loss.item())

        # Validation
        model.eval()
        with torch.no_grad():
            val_mean, val_std = model(X_v)
            val_loss = gaussian_nll_loss(val_mean, val_std, y_v).item()

        scheduler.step(val_loss)
        avg_train = np.mean(train_losses)
        logger.info(
            f"Epoch {epoch+1:3d}/{config.epochs} | Train: {avg_train:.4f} | Val: {val_loss:.4f}"
        )

        if val_loss < best_val_loss - config.min_delta:
            best_val_loss = val_loss
            patience_counter = 0
            os.makedirs(config.save_dir, exist_ok=True)
            torch.save(
                model.state_dict(), f"{config.save_dir}/{config.model_name}"
            )
            logger.info(f"  ✓ Model saved (val_loss={best_val_loss:.4f})")
        else:
            patience_counter += 1
            if patience_counter >= config.patience:
                logger.info(f"Early stopping at epoch {epoch+1}")
                break

    logger.info(f"Training complete. Best val loss: {best_val_loss:.4f}")
    return model


if __name__ == "__main__":
    # Example: train with random data for testing
    config = TrainingConfig()
    N = 500
    X_train = np.random.randn(N, config.lookback_days, config.input_size).astype(np.float32)
    y_train = np.random.randn(N, config.forecast_days).astype(np.float32) * 100 + 2500
    X_val = np.random.randn(100, config.lookback_days, config.input_size).astype(np.float32)
    y_val = np.random.randn(100, config.forecast_days).astype(np.float32) * 100 + 2500
    train(config, X_train, y_train, X_val, y_val)
