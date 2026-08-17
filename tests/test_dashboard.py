import os
import pytest
from src.visualizations.dashboard import generate_dashboard

def test_generate_dashboard_html(tmp_path):
    output_path = tmp_path / "dashboard.html"
    generate_dashboard(str(output_path))

    assert os.path.exists(output_path)
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "<html" in content
    assert "AI Economic Impact Dashboard" in content
    assert "computeData" in content
    assert "exposureData" in content
    assert "complianceData" in content
