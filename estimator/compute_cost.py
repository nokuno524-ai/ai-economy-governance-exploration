"""
Compute cost estimator module.

This module provides offline cost tables and pure functions for estimating AI training
and inference costs.
"""
from typing import Dict, Any, Union

# Cost tables for GPUs ($/GPU-hour)
# Source: Illustrative estimates based on public cloud provider pricing (e.g., AWS, GCP).
GPU_COSTS: Dict[str, Dict[str, float]] = {
    "a100": {"low": 2.5, "high": 4.5},
    "h100": {"low": 4.5, "high": 8.5},
}

# Cost tables for Inference ($/1M tokens)
# Source: Illustrative estimates based on typical API provider pricing (e.g., OpenAI, Anthropic).
INFERENCE_COSTS: Dict[str, Dict[str, float]] = {
    "small": {"input": 0.15, "output": 0.60},
    "mid": {"input": 1.00, "output": 3.00},
    "large": {"input": 5.00, "output": 15.00},
}


def estimate_training_cost(
    gpus: int, hours: float, gpu_type: str = "a100", utilization: float = 1.0
) -> Dict[str, Union[float, str]]:
    """
    Estimate AI model training cost based on GPU hours.

    Args:
        gpus: Number of GPUs used for training.
        hours: Total hours of training.
        gpu_type: The type of GPU ("a100" or "h100").
        utilization: GPU utilization factor (0.0 to 1.0), used to scale effective cost if desired.
                     Currently, it scales the required hours (lower utilization -> more hours needed).

    Returns:
        A dictionary containing the low and high cost estimates.
    """
    if hours < 0:
        raise ValueError("Hours cannot be negative.")
    if gpus < 0:
        raise ValueError("Number of GPUs cannot be negative.")
    if not (0.0 < utilization <= 1.0):
        raise ValueError("Utilization must be in the range (0.0, 1.0].")

    gpu_key = gpu_type.lower()
    fallback = False
    if gpu_key not in GPU_COSTS:
        gpu_key = "a100"  # fallback
        fallback = True

    effective_hours = hours / utilization
    total_hours = gpus * effective_hours

    low_cost = total_hours * GPU_COSTS[gpu_key]["low"]
    high_cost = total_hours * GPU_COSTS[gpu_key]["high"]

    res: Dict[str, Union[float, str]] = {
        "low_cost": low_cost,
        "high_cost": high_cost,
        "gpu_type_used": gpu_key,
    }
    if fallback:
        res["warning"] = f"Unknown GPU type '{gpu_type}'. Fell back to '{gpu_key}'."
    return res


def chars_to_tokens(chars: int) -> int:
    """
    Helper function to estimate tokens from characters.
    Uses the rough heuristic of 4 characters per token.

    Args:
        chars: Number of characters.

    Returns:
        Estimated number of tokens.
    """
    if chars < 0:
        raise ValueError("Characters cannot be negative.")
    return chars // 4


def estimate_inference_cost(
    tokens_in: int, tokens_out: int, model_class: str = "mid"
) -> Dict[str, Union[float, str]]:
    """
    Estimate inference cost based on input and output tokens.

    Args:
        tokens_in: Number of input tokens.
        tokens_out: Number of output tokens.
        model_class: The model tier ("small", "mid", "large").

    Returns:
        A dictionary with the estimated total cost.
    """
    if tokens_in < 0 or tokens_out < 0:
        raise ValueError("Tokens cannot be negative.")

    model_key = model_class.lower()
    fallback = False
    if model_key not in INFERENCE_COSTS:
        model_key = "mid"
        fallback = True

    cost_in = (tokens_in / 1_000_000) * INFERENCE_COSTS[model_key]["input"]
    cost_out = (tokens_out / 1_000_000) * INFERENCE_COSTS[model_key]["output"]
    total_cost = cost_in + cost_out

    res: Dict[str, Union[float, str]] = {
        "total_cost": total_cost,
        "model_class_used": model_key,
    }
    if fallback:
        res["warning"] = f"Unknown model class '{model_class}'. Fell back to '{model_key}'."
    return res


def amortize(total_cost: float, months: int) -> float:
    """
    Amortize a total cost over a given number of months.

    Args:
        total_cost: The total cost to amortize.
        months: The number of months.

    Returns:
        The amortized monthly cost.
    """
    if months <= 0:
        raise ValueError("Months must be greater than zero.")
    if total_cost < 0:
        raise ValueError("Total cost cannot be negative.")
    return total_cost / months
