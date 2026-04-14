"""
Tests for compute logic.
"""
import pytest
from src.models.compute import calculate_training_flops, calculate_training_cost

def test_calculate_training_flops():
    # 1B params, 1B tokens -> 6 * 1e9 * 1e9 = 6e18
    flops = calculate_training_flops(1.0, 1.0)
    assert flops == 6e18

    flops = calculate_training_flops(70.0, 15000.0)
    assert flops == 6.0 * 70e9 * 15000e9

def test_calculate_training_cost_cloud():
    result = calculate_training_cost(
        params_b=1.0,
        tokens_b=1.0,
        hardware_name="A100_80GB",
        environment="cloud",
        region="US_EAST",
        utilization_rate=0.5
    )

    assert "total_flops" in result
    assert result["total_flops"] == 6e18
    assert "total_time_hours" in result
    assert result["hourly_cost"] == 3.5  # Base A100 cost
    assert result["hardware_used"] == "A100_80GB"

def test_calculate_training_cost_on_premise():
    result = calculate_training_cost(
        params_b=1.0,
        tokens_b=1.0,
        hardware_name="A100_80GB",
        environment="on_premise",
        region="US_EAST",
        utilization_rate=0.5
    )

    assert result["hourly_cost"] == 1.5  # Base A100 on_premise cost

def test_regional_multiplier():
    result_us = calculate_training_cost(
        params_b=1.0, tokens_b=1.0, hardware_name="A100_80GB", region="US_EAST"
    )
    result_eu = calculate_training_cost(
        params_b=1.0, tokens_b=1.0, hardware_name="A100_80GB", region="EU_WEST"
    )

    assert result_eu["hourly_cost"] > result_us["hourly_cost"]
    assert result_eu["hourly_cost"] == result_us["hourly_cost"] * 1.15

def test_invalid_hardware():
    with pytest.raises(ValueError):
        calculate_training_cost(1.0, 1.0, "INVALID_GPU")

def test_invalid_environment():
    with pytest.raises(ValueError):
        calculate_training_cost(1.0, 1.0, "A100_80GB", environment="invalid")
