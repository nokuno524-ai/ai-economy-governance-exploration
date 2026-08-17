import pytest
from src.governance.compliance_engine import load_and_validate_schema, classify_use_case, get_obligations

def test_load_and_validate_schema():
    rules = load_and_validate_schema("data/governance_rules.json")
    assert "jurisdictions" in rules
    assert "EU" in rules["jurisdictions"]
    assert "US" in rules["jurisdictions"]

    with pytest.raises(FileNotFoundError):
        load_and_validate_schema("data/non_existent.json")

def test_classify_use_case():
    rules = load_and_validate_schema("data/governance_rules.json")

    system_eu_high_risk = {
        "deployment_region": ["EU"],
        "is_high_risk": True
    }
    classification = classify_use_case(system_eu_high_risk, rules)
    assert classification["EU"]["tier"] == "High Risk"

    system_eu_unacceptable = {
        "deployment_region": ["EU"],
        "uses_biometrics": True
    }
    classification = classify_use_case(system_eu_unacceptable, rules)
    assert classification["EU"]["tier"] == "Unacceptable Risk"

    system_us_foundation = {
        "deployment_region": ["US"],
        "foundation_model": True
    }
    classification = classify_use_case(system_us_foundation, rules)
    assert "Safe, Secure AI (EO 14110)" in classification["US"]["theme"]

def test_get_obligations():
    rules = load_and_validate_schema("data/governance_rules.json")

    system_eu_minimal = {
        "deployment_region": ["EU"],
        "is_high_risk": False
    }
    obligations = get_obligations(system_eu_minimal, rules)
    assert "Transparency requirements" in obligations["EU"]

    system_us_federal = {
        "deployment_region": ["US"],
        "federal_use": False
    }
    obligations = get_obligations(system_us_federal, rules)
    assert "Monitor federal preemption of state laws" in obligations["US"]
