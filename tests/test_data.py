"""
Tests for data validation.
"""
import pytest
from src.data.hardware import get_hardware, get_available_hardware, HardwareConfig
from src.data.historical import get_historical_models

def test_get_hardware():
    hw = get_hardware("H100_80GB")
    assert isinstance(hw, HardwareConfig)
    assert hw.name == "H100_80GB"
    assert hw.memory_gb == 80
    assert hw.tflops_fp16 == 989.0

def test_get_available_hardware():
    available = get_available_hardware()
    assert isinstance(available, list)
    assert "A100_80GB" in available
    assert "H100_80GB" in available

def test_get_historical_models():
    models = get_historical_models()
    assert isinstance(models, list)
    assert len(models) > 0
    assert "name" in models[0]
    assert "params_b" in models[0]
