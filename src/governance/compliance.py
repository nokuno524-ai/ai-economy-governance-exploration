"""
Governance Compliance Engine

Provides data and timelines for AI governance compliance
across different jurisdictions (e.g., EU AI Act, US EOs).

Methodology based on the EU AI Act (Regulation (EU) 2024/1689)
and US Executive Orders 14179 and 14365.
"""
import pandas as pd
from typing import Dict, Any, List

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

def check_compliance(system_description: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Check AI system compliance against regulations in specified jurisdictions.

    Args:
        system_description (Dict[str, Any]): Dictionary containing details about the AI system.
            Expected keys:
            - deployment_region (List[str]): List of regions (e.g., "EU", "US").
            - is_high_risk (bool): Whether the system is classified as high-risk.
            - uses_biometrics (bool): Whether the system uses real-time biometric identification.

    Returns:
        Dict[str, List[str]]: A dictionary with regions as keys and lists of compliance action items as values.
    """
    report = {}
    regions = system_description.get("deployment_region", [])

    if "EU" in regions:
        eu_actions = []
        if system_description.get("uses_biometrics", False):
            eu_actions.append("Prohibition: Real-time biometric identification may be prohibited under EU AI Act.")
        if system_description.get("is_high_risk", False):
            eu_actions.append("Action Required: High-Risk Full Compliance by Aug 2026-2027 (requires conformity assessment, data governance, transparency).")
        else:
            eu_actions.append("Transparency: Ensure minimal transparency requirements for limited-risk systems.")
        eu_actions.append("Action Required: Comply with GPAI Governance Rules by Aug 2025 if acting as a provider of GPAI models.")
        report["EU"] = eu_actions

    if "US" in regions:
        us_actions = []
        us_actions.append("Monitoring: Track potential federal preemption of state AI laws per US EO 14365.")
        us_actions.append("Opportunity: Leverage deregulatory stance and infrastructure focus per US EO 14179 and AI Action Plan.")
        report["US"] = us_actions

    return report
