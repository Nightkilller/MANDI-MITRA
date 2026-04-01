import sqlite3
import numpy as np
import datetime
import os
import sys
import logging
import pickle
from sklearn.preprocessing import StandardScaler

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.training.config import TrainingConfig
from ml.training.train import train

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "mandimitra.db")

def load_data_from_sqlite():
    """Extract sequences from SQLite database for training."""
    config = TrainingConfig()
    lookback = config.lookback_days
    forecast = config.forecast_days
    
    logger.info(f"Connecting to SQLite database at {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    X_all = []
    y_all = []
    
    for crop in config.crops:
        for mandi in config.mandis:
            cursor = conn.execute(
                "SELECT date, modal_price, arrival_tonnes FROM prices WHERE crop = ? AND mandi = ? ORDER BY date ASC",
                (crop, mandi)
            )
            rows = cursor.fetchall()
            
            if len(rows) < lookback + forecast:
                continue
                
            prices = np.array([r["modal_price"] for r in rows], dtype=np.float32)
            arrivals = np.array([r["arrival_tonnes"] for r in rows], dtype=np.float32)
            dates = [datetime.datetime.strptime(r["date"], "%Y-%m-%d") for r in rows]
            
            for i in range(len(rows) - lookback - forecast):
                y_seq = prices[i + lookback : i + lookback + forecast]
                
                x_window = []
                for j in range(lookback):
                    current_idx = i + j
                    dt = dates[current_idx]
                    
                    p_curr = prices[current_idx]
                    p_1 = prices[max(0, current_idx - 1)]
                    p_7 = prices[max(0, current_idx - 7)]
                    p_14 = prices[max(0, current_idx - 14)]
                    p_30 = prices[max(0, current_idx - 30)]
                    
                    arr = arrivals[current_idx]
                    
                    month_angle = 2 * np.pi * dt.month / 12
                    dow_angle = 2 * np.pi * dt.weekday() / 7
                    rain = max(0, 5 * np.sin(month_angle - np.pi/2)) 
                    temp = 30 + 10 * np.sin(month_angle - np.pi/3)   
                    
                    rolling_win = prices[max(0, current_idx - 7) : current_idx + 1]
                    mean_val = np.mean(rolling_win)
                    std_val = np.std(rolling_win) if len(rolling_win) > 1 else 0.0
                    
                    feats = [
                        p_1, p_7, p_14, p_30, arr, rain, temp,
                        np.sin(month_angle), np.cos(month_angle),
                        np.sin(dow_angle), np.cos(dow_angle),
                        mean_val, std_val
                    ]
                    x_window.append(feats)
                
                X_all.append(x_window)
                y_all.append(y_seq)
                
    conn.close()
    
    X = np.array(X_all, dtype=np.float32)
    y = np.array(y_all, dtype=np.float32)
    return config, X, y

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Starting LSTM Model Retraining Pipeline (WITH SCALER)")
    logger.info("=" * 60)
    
    config, X, y = load_data_from_sqlite()
    logger.info(f"Extracted {len(X)} training sequences of shape {X.shape[1:]}")
    
    if len(X) == 0:
        logger.error("No data extracted. Ensure database is populated.")
        sys.exit(1)
        
    # SCALING IMPLEMENTATION
    logger.info("Fitting and applying StandardScaler to features and targets...")
    num_samples, lookback, num_features = X.shape
    X_flat = X.reshape(-1, num_features)
    
    X_scaler = StandardScaler()
    X_flat_scaled = X_scaler.fit_transform(X_flat)
    X_scaled = X_flat_scaled.reshape(num_samples, lookback, num_features)
    
    y_scaler = StandardScaler()
    y_scaled = y_scaler.fit_transform(y)
    
    # Save the scalers for inference in backend/services/model_service.py
    os.makedirs(config.save_dir, exist_ok=True)
    scaler_path = f"{config.save_dir}/scaler.pkl"
    with open(scaler_path, "wb") as f:
        pickle.dump({"X_scaler": X_scaler, "y_scaler": y_scaler}, f)
    logger.info(f"Scalers saved to {scaler_path}")
        
    # Split into Train / Val
    indices = np.random.permutation(len(X_scaled))
    split_idx = int(len(X_scaled) * config.train_split)
    
    X_train, y_train = X_scaled[indices[:split_idx]], y_scaled[indices[:split_idx]]
    X_val, y_val = X_scaled[indices[split_idx:]], y_scaled[indices[split_idx:]]
    
    logger.info(f"Training set:   {len(X_train)} samples")
    logger.info(f"Validation set: {len(X_val)} samples")
    logger.info("-" * 60)
    
    # Run training loop defined in train.py
    config.epochs = 30
    model = train(config, X_train, y_train, X_val, y_val)
    
    logger.info("=" * 60)
    logger.info(f"🎉 Model Retraining Complete! Saved to {config.save_dir}/{config.model_name}")
