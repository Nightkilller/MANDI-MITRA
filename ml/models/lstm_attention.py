import torch
import torch.nn as nn
import torch.nn.functional as F


class BahdanauAttention(nn.Module):
    """Bahdanau (additive) attention over LSTM hidden states."""

    def __init__(self, hidden_size: int):
        super().__init__()
        self.W_query = nn.Linear(hidden_size, hidden_size, bias=False)
        self.W_key = nn.Linear(hidden_size, hidden_size, bias=False)
        self.V = nn.Linear(hidden_size, 1, bias=False)

    def forward(self, query: torch.Tensor, keys: torch.Tensor):
        # query: [batch, hidden]  keys: [batch, seq_len, hidden]
        query_exp = query.unsqueeze(1)  # [batch, 1, hidden]
        scores = self.V(
            torch.tanh(self.W_query(query_exp) + self.W_key(keys))
        ).squeeze(-1)  # [batch, seq_len]
        weights = F.softmax(scores, dim=-1)  # [batch, seq_len]
        context = torch.bmm(weights.unsqueeze(1), keys).squeeze(1)  # [batch, hidden]
        return context, weights


class LSTMWithAttention(nn.Module):
    """
    LSTM with Bahdanau attention for multi-step probabilistic price forecasting.
    Outputs mean + log_std for each forecast horizon (Gaussian NLL training).
    """

    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        num_layers: int,
        output_size: int,
        dropout: float = 0.2,
    ):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.input_proj = nn.Linear(input_size, hidden_size)
        self.lstm = nn.LSTM(
            hidden_size, hidden_size, num_layers, batch_first=True, dropout=dropout
        )
        self.attention = BahdanauAttention(hidden_size)
        self.dropout = nn.Dropout(dropout)

        # Output heads
        self.mean_head = nn.Sequential(
            nn.Linear(hidden_size * 2, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
        )
        self.logstd_head = nn.Sequential(
            nn.Linear(hidden_size * 2, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
        )

        self._attention_weights = None  # For XAI extraction

    def forward(self, x: torch.Tensor):
        # x: [batch, seq_len, input_size]
        x_proj = self.input_proj(x)  # [batch, seq, hidden]
        lstm_out, (h_n, _) = self.lstm(x_proj)  # lstm_out: [batch, seq, hidden]

        # Use last hidden state as query
        query = h_n[-1]  # [batch, hidden]
        context, self._attention_weights = self.attention(query, lstm_out)

        # Concat last hidden state + context
        combined = torch.cat([query, context], dim=-1)  # [batch, hidden*2]
        combined = self.dropout(combined)

        mean = self.mean_head(combined)  # [batch, output_size]
        logstd = self.logstd_head(combined)
        std = torch.exp(logstd.clamp(-3, 3))  # Prevent exploding std

        return mean, std

    def get_attention_weights(self, x: torch.Tensor) -> torch.Tensor:
        """Extract attention weights (used by XAI module)."""
        with torch.no_grad():
            self.forward(x)
        return self._attention_weights.squeeze(0)  # [seq_len]


def gaussian_nll_loss(
    mean: torch.Tensor, std: torch.Tensor, target: torch.Tensor
) -> torch.Tensor:
    """Negative log-likelihood loss for probabilistic output."""
    dist = torch.distributions.Normal(mean, std)
    return -dist.log_prob(target).mean()
