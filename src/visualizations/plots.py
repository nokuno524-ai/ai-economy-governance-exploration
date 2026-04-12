"""
Visualizations Module

Provides functions to generate visualizations for cost projections,
task exposure, and governance timelines using matplotlib and plotly.
"""
import os
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict

def plot_cost_projections(projections: Dict[int, float], output_path: str = "output/cost_projection.html"):
    """
    Plots the projected inference cost drop over time using plotly for interactivity.

    Args:
        projections (Dict[int, float]): Dictionary mapping years to cost.
        output_path (str): File path to save the plot as an HTML file.
    """
    years = list(projections.keys())
    costs = list(projections.values())

    df = pd.DataFrame({"Year": years, "Cost (USD) per 1M Tokens": costs})
    fig = px.line(df, x="Year", y="Cost (USD) per 1M Tokens", markers=True,
                  title="Projected Inference Cost Drop (10x reduction per year)",
                  log_y=True)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.write_html(output_path)

def plot_task_exposure_heatmap(exposure_df: pd.DataFrame, output_path: str = "output/task_exposure.html"):
    """
    Plots a heatmap-style bar chart of AI exposure by industry using plotly.

    Args:
        exposure_df (pd.DataFrame): DataFrame with 'Industry' and 'AI_Exposure_Score'.
        output_path (str): File path to save the plot as an HTML file.
    """
    df_sorted = exposure_df.sort_values("AI_Exposure_Score", ascending=True)

    fig = px.bar(df_sorted, x="AI_Exposure_Score", y="Industry", orientation='h',
                 color="AI_Exposure_Score",
                 color_continuous_scale="Reds",
                 title="AI Task Exposure by Industry")

    fig.update_layout(xaxis_title="Exposure Score (0.0 - 1.0)", yaxis_title="")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.write_html(output_path)

def plot_governance_timeline(timeline_df: pd.DataFrame, output_path: str = "output/governance_timeline.html"):
    """
    Plots a timeline of governance compliance using plotly.

    Args:
        timeline_df (pd.DataFrame): DataFrame with 'Milestone', 'Date', and 'Jurisdiction'.
        output_path (str): File path to save the plot as an HTML file.
    """
    timeline_df = timeline_df.sort_values("Date")

    fig = px.scatter(timeline_df, x="Date", y="Jurisdiction", color="Regulation",
                     text="Milestone", title="AI Governance Compliance Timeline",
                     size_max=15)

    fig.update_traces(textposition='top center', marker=dict(size=12))
    fig.update_layout(xaxis_title="Date", yaxis_title="Jurisdiction", showlegend=True,
                      height=600)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.write_html(output_path)
