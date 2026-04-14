"""
Historical data points for AI models and scaling.
"""
from typing import Dict, Any, List

# Historical model data: name, params (billions), tokens (billions), release year, estimated training cost
HISTORICAL_MODELS = [
    {
        "name": "GPT-3",
        "params_b": 175.0,
        "tokens_b": 300.0,
        "year": 2020,
        "est_cost_m": 4.6
    },
    {
        "name": "LLaMA-1 (65B)",
        "params_b": 65.0,
        "tokens_b": 1400.0,
        "year": 2023,
        "est_cost_m": 2.0
    },
    {
        "name": "GPT-4 (Estimated)",
        "params_b": 1800.0,
        "tokens_b": 13000.0,
        "year": 2023,
        "est_cost_m": 78.0
    },
    {
        "name": "Llama-3 (70B)",
        "params_b": 70.0,
        "tokens_b": 15000.0,
        "year": 2024,
        "est_cost_m": 12.0
    }
]

def get_historical_models() -> List[Dict[str, Any]]:
    """Return list of historical model data points."""
    return HISTORICAL_MODELS
