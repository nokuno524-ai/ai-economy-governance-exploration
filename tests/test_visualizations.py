import pytest
import os
import pandas as pd
from src.visualizations.plots import plot_cost_projections, plot_task_exposure_heatmap, plot_governance_timeline

def test_plot_cost_projections(tmp_path):
    output_path = tmp_path / "test_cost_proj.html"
    projections = {0: 10.0, 1: 1.0, 2: 0.1}
    plot_cost_projections(projections, str(output_path))
    assert os.path.exists(output_path)

def test_plot_task_exposure_heatmap(tmp_path):
    output_path = tmp_path / "test_task_exp.html"
    df = pd.DataFrame({
        "Industry": ["A", "B"],
        "AI_Exposure_Score": [0.1, 0.9],
        "Skill_Level": ["High", "Low"]
    })
    plot_task_exposure_heatmap(df, str(output_path))
    assert os.path.exists(output_path)

def test_plot_governance_timeline(tmp_path):
    output_path = tmp_path / "test_gov_time.html"
    df = pd.DataFrame({
        "Regulation": ["R1", "R2"],
        "Milestone": ["M1", "M2"],
        "Date": ["2025-01-01", "2025-02-01"],
        "Jurisdiction": ["J1", "J2"]
    })
    df['Date'] = pd.to_datetime(df['Date'])
    plot_governance_timeline(df, str(output_path))
    assert os.path.exists(output_path)
