import pytest
import subprocess
import os

def test_cli_help():
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    result = subprocess.run(['python3', 'src/cli.py', '--help'], capture_output=True, text=True, env=env)
    assert result.returncode == 0
    assert "AI Economic Impact Dashboard CLI" in result.stdout

def test_cli_compute_training():
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    result = subprocess.run(['python3', 'src/cli.py', 'compute', 'training', '--params', '1', '--tokens', '1'], capture_output=True, text=True, env=env)
    assert result.returncode == 0
    assert "total_flops" in result.stdout

def test_cli_compute_inference():
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    result = subprocess.run(['python3', 'src/cli.py', 'compute', 'inference', '--current-cost', '10', '--years', '2'], capture_output=True, text=True, env=env)
    assert result.returncode == 0
    assert "10.0" in result.stdout

def test_cli_compute_tco():
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    result = subprocess.run(['python3', 'src/cli.py', 'compute', 'tco', '--tokens-monthly', '100', '--api-cost', '0.5', '--hardware-monthly', '1000', '--ops-monthly', '500'], capture_output=True, text=True, env=env)
    assert result.returncode == 0
    assert "Cloud API" in result.stdout
    assert "Self-Hosted" in result.stdout
    assert "Hybrid" in result.stdout
