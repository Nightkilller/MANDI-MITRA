from dataclasses import dataclass, field
from typing import List


@dataclass
class TrainingConfig:
    # Data
    crops: List[str] = field(default_factory=lambda: ["tomato", "onion", "wheat", "soybean"])
    mandis: List[str] = field(default_factory=lambda: ["indore", "bhopal", "ujjain", "jabalpur", "sagar"])
    lookback_days: int = 30
    forecast_days: int = 14
    train_split: float = 0.80
    val_split: float = 0.10

    # Model architecture
    input_size: int = 13
    hidden_size: int = 128
    num_layers: int = 2
    output_size: int = 14
    dropout: float = 0.2

    # Training
    epochs: int = 100
    batch_size: int = 32
    learning_rate: float = 0.001
    weight_decay: float = 1e-5
    patience: int = 15
    min_delta: float = 0.001

    # Paths
    save_dir: str = "./ml/saved_models"
    model_name: str = "lstm_attention_v1.pt"
