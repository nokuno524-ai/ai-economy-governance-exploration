"""
Compute cost estimation models and logic.
"""
from typing import Dict, Any
from src.data.hardware import get_hardware, REGIONAL_PRICING_MULTIPLIERS

def calculate_training_flops(params_b: float, tokens_b: float) -> float:
    """
    Calculate the total FLOPs required for training.
    Formula: ~6 * parameters * tokens (standard Kaplan scaling law approximation).

    Args:
        params_b: Number of parameters in billions.
        tokens_b: Number of training tokens in billions.

    Returns:
        Total FLOPs required.
    """
    params = params_b * 1e9
    tokens = tokens_b * 1e9
    return 6.0 * params * tokens

def calculate_training_cost(
    params_b: float,
    tokens_b: float,
    hardware_name: str,
    environment: str = "cloud",
    region: str = "US_EAST",
    utilization_rate: float = 0.4
) -> Dict[str, Any]:
    """
    Calculate the estimated cost and time to train a model.

    Args:
        params_b: Number of parameters in billions.
        tokens_b: Number of training tokens in billions.
        hardware_name: The target hardware configuration (e.g., "A100_80GB").
        environment: "cloud" or "on_premise".
        region: Region code for pricing multiplier.
        utilization_rate: Hardware Model FLOPs Utilization (MFU), typically 0.3 to 0.5.

    Returns:
        Dictionary containing estimated cost, total hours, and other metrics.
    """
    hardware = get_hardware(hardware_name)
    total_flops = calculate_training_flops(params_b, tokens_b)

    # Calculate achieved TFLOPs per second based on utilization
    achieved_tflops_s = hardware.tflops_fp16 * utilization_rate
    achieved_flops_s = achieved_tflops_s * 1e12

    # Calculate time in seconds, then hours
    total_time_seconds = total_flops / achieved_flops_s if achieved_flops_s > 0 else 0
    total_time_hours = total_time_seconds / 3600.0

    # Determine base cost per hour
    if environment.lower() == "cloud":
        base_cost = hardware.hourly_cost_cloud
    elif environment.lower() == "on_premise":
        base_cost = hardware.hourly_cost_on_premise
    else:
        raise ValueError("Environment must be 'cloud' or 'on_premise'")

    # Apply regional multiplier
    multiplier = REGIONAL_PRICING_MULTIPLIERS.get(region.upper(), 1.0)
    hourly_cost = base_cost * multiplier

    total_cost = total_time_hours * hourly_cost

    return {
        "total_flops": total_flops,
        "total_time_hours": total_time_hours,
        "total_time_days": total_time_hours / 24.0,
        "hourly_cost": hourly_cost,
        "total_cost": total_cost,
        "hardware_used": hardware_name,
        "utilization_rate": utilization_rate
    }
