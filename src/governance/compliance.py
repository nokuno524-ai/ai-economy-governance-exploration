"""
Governance Compliance Engine

Provides data and timelines for AI governance compliance
across different jurisdictions (e.g., EU AI Act, US EOs).
"""
import pandas as pd

def get_compliance_timeline() -> pd.DataFrame:
    """
    Returns data for major AI governance compliance milestones.

    Returns:
        pd.DataFrame: DataFrame containing regulation, milestone, and date.
    """
    data = {
        "Regulation": [
            "EU AI Act", "EU AI Act", "EU AI Act",
            "US EO 14179", "US AI Action Plan", "US EO 14365"
        ],
        "Milestone": [
            "Prohibitions Effective",
            "GPAI Governance Rules",
            "High-Risk Full Compliance",
            "Deregulatory Stance Effective",
            "Infrastructure Focus",
            "Preempts State AI Laws"
        ],
        "Date": [
            "2025-02-01",
            "2025-08-01",
            "2026-08-01",
            "2025-01-01",
            "2025-07-01",
            "2025-12-01"
        ],
        "Jurisdiction": ["EU", "EU", "EU", "US", "US", "US"]
    }
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def filter_by_jurisdiction(df: pd.DataFrame, jurisdiction: str) -> pd.DataFrame:
    """
    Filter the compliance timeline by jurisdiction.

    Args:
        df (pd.DataFrame): The compliance timeline data.
        jurisdiction (str): The jurisdiction to filter by (e.g., 'EU', 'US').

    Returns:
        pd.DataFrame: Filtered timeline data.
    """
    return df[df['Jurisdiction'] == jurisdiction]
