"""
Tests for CLI integration.
"""
import subprocess
import json
import os

def get_env():
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    return env

def test_cli_help():
    result = subprocess.run(
        ["python3", "src/cli.py", "--help"],
        capture_output=True,
        text=True,
        env=get_env()
    )
    assert result.returncode == 0
    assert "AI Economic Impact Dashboard" in result.stdout

def test_cli_estimate():
    result = subprocess.run(
        ["python3", "src/cli.py", "estimate", "--params", "70", "--tokens", "15000", "--json"],
        capture_output=True,
        text=True,
        env=get_env()
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "total_cost" in data
    assert data["hardware_used"] == "H100_80GB" # default

def test_cli_visualize():
    result = subprocess.run(
        ["python3", "src/cli.py", "visualize"],
        capture_output=True,
        text=True,
        env=get_env()
    )
    assert result.returncode == 0
    assert "Generating visualizations" in result.stdout
