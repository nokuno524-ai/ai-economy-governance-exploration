import pytest
from src.analyzers.compute_cost import estimate_training_cost, project_inference_cost, compare_tco

def test_estimate_training_cost():
    res = estimate_training_cost(params_billions=1.0, tokens_trillions=1.0)
    assert 'total_flops' in res
    assert 'gpu_hours' in res
    assert 'total_cost_usd' in res
    assert 'energy_consumption_kwh' in res
    assert 'tpu_pod_years' in res
    assert res['total_flops'] == 6e21

def test_project_inference_cost():
    res = project_inference_cost(10.0, 3)
    assert len(res) == 4
    assert res[0] == 10.0
    assert res[1] == 1.0
    assert res[2] == 0.1
    assert res[3] == 0.01

def test_compare_tco():
    res = compare_tco(100.0, 0.5, 1000.0, 500.0, 0.2)
    assert 'Cloud API' in res
    assert 'Self-Hosted' in res
    assert 'Hybrid' in res
    assert res['Cloud API'] == 50.0
    assert res['Self-Hosted'] == 1500.0
    assert res['Hybrid'] == (20.0 * 0.5) + 1500.0
