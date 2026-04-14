"""
Visualization functions using Plotly.
"""
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Dict, Any
from src.data.historical import get_historical_models
from src.data.hardware import HARDWARE_DATA, REGIONAL_PRICING_MULTIPLIERS
from src.models.compute import calculate_training_cost

OUTPUT_DIR = "output"

def ensure_output_dir():
    """Ensure the output directory exists."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def plot_cost_projections():
    """
    Generate an interactive plot of historical estimated training costs over time.
    """
    ensure_output_dir()
    historical = get_historical_models()

    # Sort by year
    historical.sort(key=lambda x: x["year"])

    years = [model["year"] for model in historical]
    costs = [model["est_cost_m"] for model in historical]
    names = [model["name"] for model in historical]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years,
        y=costs,
        mode='lines+markers+text',
        text=names,
        textposition="top center",
        marker=dict(size=10, color='blue'),
        line=dict(color='blue', dash='dash')
    ))

    fig.update_layout(
        title="Historical AI Model Training Costs Over Time",
        xaxis_title="Year",
        yaxis_title="Estimated Cost (Millions USD)",
        yaxis_type="log",
        template="plotly_white"
    )

    filepath = os.path.join(OUTPUT_DIR, "cost_projections.html")
    fig.write_html(filepath)
    return filepath

def plot_cost_per_parameter(target_tokens_b: float = 3000.0, hardware: str = "H100_80GB"):
    """
    Generate a plot showing the scaling of cost per parameter size.

    Args:
        target_tokens_b: Fixed tokens to calculate scaling over parameter sizes.
        hardware: Hardware used for the estimation.
    """
    ensure_output_dir()
    param_sizes_b = [1, 7, 13, 30, 70, 175, 500, 1000]
    costs = []

    for p in param_sizes_b:
        result = calculate_training_cost(
            params_b=p,
            tokens_b=target_tokens_b,
            hardware_name=hardware,
            environment="cloud"
        )
        costs.append(result["total_cost"] / 1e6) # In millions

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=param_sizes_b,
        y=costs,
        mode='lines+markers',
        marker=dict(size=8, color='green'),
        line=dict(color='green')
    ))

    fig.update_layout(
        title=f"Cost Scaling by Parameter Size ({target_tokens_b}B tokens on {hardware})",
        xaxis_title="Parameters (Billions)",
        yaxis_title="Estimated Training Cost (Millions USD)",
        xaxis_type="log",
        yaxis_type="log",
        template="plotly_white"
    )

    filepath = os.path.join(OUTPUT_DIR, "cost_per_parameter.html")
    fig.write_html(filepath)
    return filepath

def plot_regional_comparisons(params_b: float = 70.0, tokens_b: float = 15000.0, hardware: str = "H100_80GB"):
    """
    Generate a bar chart comparing costs across different regions.
    """
    ensure_output_dir()
    regions = list(REGIONAL_PRICING_MULTIPLIERS.keys())
    costs = []

    for r in regions:
        result = calculate_training_cost(
            params_b=params_b,
            tokens_b=tokens_b,
            hardware_name=hardware,
            environment="cloud",
            region=r
        )
        costs.append(result["total_cost"] / 1e6) # In millions

    fig = go.Figure(data=[
        go.Bar(name='Cloud Training Cost', x=regions, y=costs, marker_color='orange')
    ])

    fig.update_layout(
        title=f"Regional Training Cost Comparison ({params_b}B params, {tokens_b}B tokens, {hardware})",
        xaxis_title="Region",
        yaxis_title="Estimated Cost (Millions USD)",
        template="plotly_white"
    )

    filepath = os.path.join(OUTPUT_DIR, "regional_comparison.html")
    fig.write_html(filepath)
    return filepath
