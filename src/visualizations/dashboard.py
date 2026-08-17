import json
import os
from src.analyzers.compute_cost import project_inference_cost
from src.analyzers.task_exposure import analyze_task_exposure_rubric
from src.governance.compliance_engine import load_and_validate_schema, classify_use_case, get_obligations

def generate_dashboard(output_path: str = "output/dashboard.html"):
    """
    Generates a single self-contained offline HTML file containing a tabbed UI
    with the compute cost estimator, exposure analyzer, and compliance engine.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 1. Compute Cost Projection
    projections = project_inference_cost(0.48, 5)
    compute_data = json.dumps(projections)

    # 2. Exposure Analyzer
    try:
        ranked_occupations = analyze_task_exposure_rubric()
        exposure_data = json.dumps(ranked_occupations)
    except Exception as e:
        exposure_data = json.dumps({"error": str(e)})

    # 3. Compliance Engine
    try:
        rules = load_and_validate_schema()
        # Mock use case for dashboard
        mock_system = {
            "deployment_region": ["EU", "US"],
            "is_high_risk": True,
            "foundation_model": True
        }
        classification = classify_use_case(mock_system, rules)
        obligations = get_obligations(mock_system, rules)
        compliance_data = json.dumps({
            "mock_system": mock_system,
            "classification": classification,
            "obligations": obligations
        })
    except Exception as e:
        compliance_data = json.dumps({"error": str(e)})

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Economic Impact Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .tab {{ overflow: hidden; border: 1px solid #ccc; background-color: #f1f1f1; }}
        .tab button {{ background-color: inherit; float: left; border: none; outline: none; cursor: pointer; padding: 14px 16px; transition: 0.3s; }}
        .tab button:hover {{ background-color: #ddd; }}
        .tab button.active {{ background-color: #ccc; }}
        .tabcontent {{ display: none; padding: 6px 12px; border: 1px solid #ccc; border-top: none; }}
        pre {{ background: #eee; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>

    <h2>AI Economic Impact Dashboard</h2>

    <div class="tab">
      <button class="tablinks" onclick="openTab(event, 'Compute')" id="defaultOpen">Compute Cost Estimator</button>
      <button class="tablinks" onclick="openTab(event, 'Exposure')">Task Exposure Analyzer</button>
      <button class="tablinks" onclick="openTab(event, 'Compliance')">Governance Compliance Engine</button>
    </div>

    <div id="Compute" class="tabcontent">
      <h3>Projected Inference Cost (LLMflation)</h3>
      <p>Data based on 10x reduction per year.</p>
      <pre id="compute_data"></pre>
    </div>

    <div id="Exposure" class="tabcontent">
      <h3>Task Exposure Rankings</h3>
      <p>Occupations ranked by exposure score (using heuristic rubric).</p>
      <pre id="exposure_data"></pre>
    </div>

    <div id="Compliance" class="tabcontent">
      <h3>Compliance Report (Mock System)</h3>
      <p>Classification and obligations for a mock High-Risk Foundation Model deployed in EU and US.</p>
      <pre id="compliance_data"></pre>
    </div>

    <script>
        const computeData = {compute_data};
        const exposureData = {exposure_data};
        const complianceData = {compliance_data};

        document.getElementById('compute_data').textContent = JSON.stringify(computeData, null, 2);
        document.getElementById('exposure_data').textContent = JSON.stringify(exposureData, null, 2);
        document.getElementById('compliance_data').textContent = JSON.stringify(complianceData, null, 2);

        function openTab(evt, tabName) {{
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tabcontent");
            for (i = 0; i < tabcontent.length; i++) {{
                tabcontent[i].style.display = "none";
            }}
            tablinks = document.getElementsByClassName("tablinks");
            for (i = 0; i < tablinks.length; i++) {{
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }}
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        }}

        // Get the element with id="defaultOpen" and click on it
        document.getElementById("defaultOpen").click();
    </script>
</body>
</html>
"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Interactive Dashboard created at: {output_path}")
