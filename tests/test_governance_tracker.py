import pytest
from src.governance.tracker import (
    AIRegulation,
    get_regulations,
    get_regulation,
    compare_regulations,
    generate_compliance_checklist
)

def test_regulation_schema():
    reg = AIRegulation(
        id="test_id",
        name="Test Regulation",
        jurisdiction="Test Land",
        scope=["AI systems"],
        enforcement="Test Authority",
        compliance_requirements=["Do no harm"]
    )
    assert reg.id == "test_id"
    assert reg.name == "Test Regulation"
    assert reg.jurisdiction == "Test Land"
    assert "AI systems" in reg.scope
    assert reg.enforcement == "Test Authority"
    assert "Do no harm" in reg.compliance_requirements

def test_dataset_loading():
    regs = get_regulations()
    assert len(regs) >= 20

    # Check a specific regulation
    eu_act = get_regulation("eu_ai_act")
    assert eu_act.name == "EU AI Act"
    assert eu_act.jurisdiction == "European Union"

def test_get_regulation_not_found():
    with pytest.raises(ValueError):
        get_regulation("non_existent_id")

def test_compare_regulations():
    # Comparing EU AI Act and Brazil AI Bill which both have high-risk concepts
    comparison = compare_regulations(["eu_ai_act", "brazil_pl_2338"])

    assert "overlaps" in comparison
    assert "gaps" in comparison

    # Check that Transparency is in all requirements or common requirements
    assert "Transparency requirements" in comparison["all_requirements"]
    assert "Transparency" in comparison["all_requirements"]

def test_compare_regulations_empty():
    comparison = compare_regulations([])
    assert len(comparison["overlaps"]) == 0
    assert len(comparison["gaps"]) == 0

def test_generate_compliance_checklist():
    checklist = generate_compliance_checklist(["eu_ai_act", "us_eo_14110"])

    assert "EU AI Act" in checklist
    assert "US Executive Order 14110 on Safe, Secure, and Trustworthy AI" in checklist

    assert "Conformity assessments" in checklist["EU AI Act"]
    assert "Red-teaming tests reporting" in checklist["US Executive Order 14110 on Safe, Secure, and Trustworthy AI"]
