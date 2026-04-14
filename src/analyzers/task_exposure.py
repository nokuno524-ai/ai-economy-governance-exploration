"""
Task Exposure Analyzer

Provides data and functions to map AI capabilities to occupational task exposure,
showing which industries are most affected by AI automation.
"""
import pandas as pd

def get_industry_exposure_data() -> pd.DataFrame:
    """
    Returns mock data for industry-level task exposure to AI.

    Data represents percentage of tasks in each industry that are highly exposed
    to AI automation or augmentation.

    Returns:
        pd.DataFrame: DataFrame containing industries and their exposure scores.
    """
    data = {
        "Industry": [
            "Legal Services",
            "Financial Analysis",
            "Software Development",
            "Customer Support",
            "Healthcare (Admin)",
            "Healthcare (Clinical)",
            "Construction",
            "Agriculture"
        ],
        "AI_Exposure_Score": [0.75, 0.65, 0.80, 0.70, 0.55, 0.20, 0.10, 0.05],
        "Worker_Type": [
            "Knowledge",
            "Knowledge",
            "Knowledge",
            "Knowledge",
            "Knowledge",
            "Physical/Interpersonal",
            "Physical",
            "Physical"
        ]
    }
    return pd.DataFrame(data)

def analyze_exposure_by_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyzes average AI exposure score by worker type.

    Args:
        df (pd.DataFrame): DataFrame containing exposure data.

    Returns:
        pd.DataFrame: Grouped DataFrame showing average exposure per worker type.
    """
    return df.groupby("Worker_Type")["AI_Exposure_Score"].mean().reset_index()
