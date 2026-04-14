import pytest
from src.analyzers.task_exposure import estimate_exposure, get_industry_exposure_data

def test_estimate_exposure_high():
    occupation_tasks = [
        {"task": "data entry", "required_capabilities": ["text_processing"]},
        {"task": "document review", "required_capabilities": ["text_processing", "reasoning"]}
    ]
    ai_benchmarks = {
        "text_processing": 0.9,
        "reasoning": 0.85
    }
    score = estimate_exposure(occupation_tasks, ai_benchmarks)
    assert score == 1.0

def test_estimate_exposure_low():
    occupation_tasks = [
        {"task": "pipe fitting", "required_capabilities": ["physical_dexterity", "spatial_reasoning"]},
        {"task": "site inspection", "required_capabilities": ["vision", "mobility"]}
    ]
    ai_benchmarks = {
        "physical_dexterity": 0.1,
        "spatial_reasoning": 0.3,
        "vision": 0.8,
        "mobility": 0.2
    }
    score = estimate_exposure(occupation_tasks, ai_benchmarks)
    # The first task's avg score is 0.2 (0.1, 0.3).
    # The second task's avg score is 0.5 (0.8, 0.2).
    # Neither exceeds the 0.7 threshold, so score is 0.0.
    assert score == 0.0

def test_estimate_exposure_empty():
    assert estimate_exposure([], {}) == 0.0

def test_get_industry_exposure_data():
    df = get_industry_exposure_data()
    assert "Industry" in df.columns
    assert "AI_Exposure_Score" in df.columns
    assert "Skill_Level" in df.columns
    assert len(df) > 0
