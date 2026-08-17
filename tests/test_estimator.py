"""
Unit tests for the estimator package.
"""

import pytest

from estimator.compute_cost import estimate_training_cost, estimate_inference_cost, chars_to_tokens, amortize
from estimator.task_exposure import compute_occupation_exposure, rank_occupations, aggregate_sector_exposure


def test_estimate_training_cost_valid():
    res = estimate_training_cost(8, 10.0, "a100", 1.0)
    assert res["gpu_type_used"] == "a100"
    assert res["low_cost"] == 80.0 * 2.5
    assert res["high_cost"] == 80.0 * 4.5
    assert "warning" not in res


def test_estimate_training_cost_fallback():
    res = estimate_training_cost(4, 5.0, "unknown_gpu")
    assert res["gpu_type_used"] == "a100"
    assert "warning" in res


def test_estimate_training_cost_utilization():
    res = estimate_training_cost(1, 10.0, "a100", 0.5)
    # Effective hours = 10 / 0.5 = 20
    assert res["low_cost"] == 20 * 2.5


def test_estimate_training_cost_invalid():
    with pytest.raises(ValueError):
        estimate_training_cost(-1, 10.0)
    with pytest.raises(ValueError):
        estimate_training_cost(1, -10.0)
    with pytest.raises(ValueError):
        estimate_training_cost(1, 10.0, utilization=0.0)
    with pytest.raises(ValueError):
        estimate_training_cost(1, 10.0, utilization=1.5)


def test_estimate_inference_cost_valid():
    res = estimate_inference_cost(1_000_000, 2_000_000, "small")
    assert res["model_class_used"] == "small"
    # 1M input * 0.15 + 2M output * 0.60
    assert res["total_cost"] == pytest.approx(0.15 + 1.20)
    assert "warning" not in res


def test_estimate_inference_cost_fallback():
    res = estimate_inference_cost(1_000_000, 1_000_000, "unknown")
    assert res["model_class_used"] == "mid"
    assert "warning" in res


def test_estimate_inference_cost_invalid():
    with pytest.raises(ValueError):
        estimate_inference_cost(-1, 100)
    with pytest.raises(ValueError):
        estimate_inference_cost(100, -1)


def test_chars_to_tokens():
    assert chars_to_tokens(100) == 25
    assert chars_to_tokens(0) == 0
    with pytest.raises(ValueError):
        chars_to_tokens(-10)


def test_amortize():
    assert amortize(120.0, 12) == 10.0
    with pytest.raises(ValueError):
        amortize(100.0, 0)
    with pytest.raises(ValueError):
        amortize(-100.0, 12)


def test_compute_occupation_exposure():
    # Valid tasks
    tasks = [{"exposure": 0.5}, {"exposure": 1.0}]
    assert compute_occupation_exposure(tasks) == 0.75

    # Empty tasks
    assert compute_occupation_exposure([]) == 0.0

    # Invalid exposure
    with pytest.raises(ValueError):
        compute_occupation_exposure([{"exposure": 1.5}])
    with pytest.raises(ValueError):
        compute_occupation_exposure([{"exposure": -0.5}])


def test_rank_occupations():
    data = {
        "JobA": {"tasks": [{"exposure": 0.8}]},
        "JobB": {"tasks": [{"exposure": 0.4}]},
        "JobC": {"tasks": [{"exposure": 0.9}]},
    }
    ranked = rank_occupations(data)
    assert ranked == [("JobC", 0.9), ("JobA", 0.8), ("JobB", 0.4)]


def test_aggregate_sector_exposure():
    data = {
        "JobA": {"sector": "Tech", "tasks": [{"exposure": 0.8}]},
        "JobB": {"sector": "Tech", "tasks": [{"exposure": 0.4}]},
        "JobC": {"sector": "Health", "tasks": [{"exposure": 0.9}]},
        "JobD": {"sector": "Health", "tasks": []},
    }
    agg = aggregate_sector_exposure(data)
    assert agg["Tech"] == pytest.approx(0.6)
    assert agg["Health"] == pytest.approx(0.45) # (0.9 + 0.0) / 2
