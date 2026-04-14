"""
Task Exposure Analyzer

Provides data and functions to map AI capabilities to occupational task exposure,
showing which industries and skill levels are most affected by AI automation.

Methodology based on Brynjolfsson, Li & Raymond (2023) and Acemoglu's task-based framework.
Data sources conceptually mapped from O*NET task descriptions and AI benchmarks.
"""
import pandas as pd
from typing import List, Dict, Any

def get_industry_exposure_data() -> pd.DataFrame:
    """
    Returns mock data for industry-level task exposure to AI.

    Data represents percentage of tasks in each industry that are highly exposed
    to AI automation or augmentation.

    Returns:
        pd.DataFrame: DataFrame containing industries, their exposure scores, and skill levels.
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
        ],
        "Skill_Level": [
            "High",
            "High",
            "High",
            "Medium",
            "Medium",
            "High",
            "Medium",
            "Low"
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

def estimate_exposure(occupation_tasks: List[Dict[str, Any]], ai_benchmarks: Dict[str, float]) -> float:
    """
    Estimates the AI automation exposure for a given occupation.

    Methodology:
    Iterates through the list of tasks for an occupation (mapped from O*NET).
    For each task, checks its required capabilities against AI benchmark scores.
    If the average benchmark score for required capabilities exceeds a threshold (e.g., 0.7),
    the task is considered exposed.

    Args:
        occupation_tasks (List[Dict[str, Any]]): List of tasks. Each task is a dict, e.g.,
            {"task": "data entry", "required_capabilities": ["text_processing", "vision"]}
        ai_benchmarks (Dict[str, float]): Dictionary of AI capability scores, e.g.,
            {"text_processing": 0.9, "vision": 0.8, "physical_dexterity": 0.1}

    Returns:
        float: The ratio of exposed tasks to total tasks (0.0 to 1.0).
    """
    if not occupation_tasks:
        return 0.0

    exposed_tasks = 0
    threshold = 0.7

    for task in occupation_tasks:
        capabilities = task.get("required_capabilities", [])
        if not capabilities:
            continue

        scores = [ai_benchmarks.get(cap, 0.0) for cap in capabilities]
        avg_score = sum(scores) / len(scores)

        if avg_score >= threshold:
            exposed_tasks += 1

    return exposed_tasks / len(occupation_tasks)
