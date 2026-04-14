import pytest
from src.governance.compliance import check_compliance, get_compliance_timeline

def test_check_compliance_eu_high_risk():
    system = {
        "deployment_region": ["EU"],
        "is_high_risk": True,
        "uses_biometrics": False
    }
    report = check_compliance(system)
    assert "EU" in report
    assert any("High-Risk Full Compliance" in item for item in report["EU"])
    assert not any("Prohibition" in item for item in report["EU"])

def test_check_compliance_eu_biometrics():
    system = {
        "deployment_region": ["EU"],
        "is_high_risk": False,
        "uses_biometrics": True
    }
    report = check_compliance(system)
    assert "EU" in report
    assert any("Prohibition: Real-time biometric identification" in item for item in report["EU"])

def test_check_compliance_us():
    system = {
        "deployment_region": ["US"]
    }
    report = check_compliance(system)
    assert "US" in report
    assert any("US EO 14365" in item for item in report["US"])
    assert any("US EO 14179" in item for item in report["US"])

def test_check_compliance_multiple_regions():
    system = {
        "deployment_region": ["EU", "US"],
        "is_high_risk": True,
        "uses_biometrics": True
    }
    report = check_compliance(system)
    assert "EU" in report
    assert "US" in report
    assert any("Prohibition" in item for item in report["EU"])
    assert any("US EO 14179" in item for item in report["US"])

def test_get_compliance_timeline():
    df = get_compliance_timeline()
    assert "Regulation" in df.columns
    assert "Jurisdiction" in df.columns
    assert len(df) > 0
