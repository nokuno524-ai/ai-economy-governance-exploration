"""
Hardware configuration and pricing data for compute estimates.
"""
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class HardwareConfig:
    """Hardware configuration properties."""
    name: str
    tflops_fp16: float
    memory_gb: int
    hourly_cost_cloud: float
    hourly_cost_on_premise: float

HARDWARE_DATA = {
    "A100_80GB": HardwareConfig(
        name="A100_80GB",
        tflops_fp16=312.0,
        memory_gb=80,
        hourly_cost_cloud=3.5,
        hourly_cost_on_premise=1.5
    ),
    "H100_80GB": HardwareConfig(
        name="H100_80GB",
        tflops_fp16=989.0,
        memory_gb=80,
        hourly_cost_cloud=8.5,
        hourly_cost_on_premise=3.0
    ),
    "B200": HardwareConfig(
        name="B200",
        tflops_fp16=4500.0, # Estimated
        memory_gb=192,
        hourly_cost_cloud=15.0, # Estimated
        hourly_cost_on_premise=6.0 # Estimated
    )
}

REGIONAL_PRICING_MULTIPLIERS = {
    "US_EAST": 1.0,
    "US_WEST": 1.0,
    "EU_WEST": 1.15,
    "ASIA_PACIFIC": 1.2
}

def get_hardware(name: str) -> HardwareConfig:
    """Retrieve hardware config by name."""
    if name not in HARDWARE_DATA:
        raise ValueError(f"Hardware '{name}' not found. Available: {list(HARDWARE_DATA.keys())}")
    return HARDWARE_DATA[name]

def get_available_hardware() -> List[str]:
    """Return a list of available hardware options."""
    return list(HARDWARE_DATA.keys())
