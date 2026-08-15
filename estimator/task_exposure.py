"""
Task exposure analyzer module.

This module provides tools to analyze automation exposure scores for different
occupations and aggregate them to the sector level.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Path to the bundled tasks.json file
TASKS_JSON_PATH = Path(__file__).parent / "tasks.json"


def load_tasks_data() -> Dict[str, Any]:
    """
    Load the tasks data from the bundled JSON file.

    Returns:
        A dictionary containing the tasks data.
    """
    if not TASKS_JSON_PATH.exists():
        raise FileNotFoundError(f"Could not find {TASKS_JSON_PATH}")
    with open(TASKS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_occupation_exposure(tasks: List[Dict[str, Any]]) -> float:
    """
    Compute the average automation exposure score for an occupation based on its tasks.

    Args:
        tasks: A list of task dictionaries, each containing an 'exposure' score (0-1).

    Returns:
        The average exposure score (0.0 to 1.0). If the task list is empty, returns 0.0.
    """
    if not tasks:
        return 0.0

    total_exposure = 0.0
    for task in tasks:
        exposure = task.get("exposure", 0.0)
        if not (0.0 <= exposure <= 1.0):
            raise ValueError(f"Exposure score {exposure} is out of bounds [0, 1].")
        total_exposure += exposure

    return total_exposure / len(tasks)


def rank_occupations(data: Dict[str, Any]) -> List[Tuple[str, float]]:
    """
    Rank occupations by their overall exposure score in descending order.

    Args:
        data: The tasks data dictionary containing occupations and their tasks.

    Returns:
        A list of tuples (occupation_name, exposure_score), sorted by score descending.
    """
    rankings: List[Tuple[str, float]] = []
    for occupation, details in data.items():
        tasks = details.get("tasks", [])
        score = compute_occupation_exposure(tasks)
        rankings.append((occupation, score))

    rankings.sort(key=lambda x: x[1], reverse=True)
    return rankings


def aggregate_sector_exposure(data: Dict[str, Any]) -> Dict[str, float]:
    """
    Aggregate and average exposure scores at the sector level.

    Args:
        data: The tasks data dictionary containing occupations, sectors, and tasks.

    Returns:
        A dictionary mapping sector names to their average exposure score.
    """
    sector_scores: Dict[str, List[float]] = {}
    for occupation, details in data.items():
        sector = details.get("sector", "Unknown")
        tasks = details.get("tasks", [])
        score = compute_occupation_exposure(tasks)
        if sector not in sector_scores:
            sector_scores[sector] = []
        sector_scores[sector].append(score)

    aggregated: Dict[str, float] = {}
    for sector, scores in sector_scores.items():
        if scores:
            aggregated[sector] = sum(scores) / len(scores)
        else:
            aggregated[sector] = 0.0
    return aggregated
