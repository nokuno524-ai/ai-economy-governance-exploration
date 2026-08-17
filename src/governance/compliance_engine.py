import json
import os
from typing import Dict, Any, List

def load_and_validate_schema(filepath: str = "data/governance_rules.json") -> Dict[str, Any]:
    """
    Loads and validates the JSON schema for governance rules.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not find {filepath}")

    with open(filepath, 'r') as f:
        data = json.load(f)

    if "jurisdictions" not in data:
        raise ValueError("Invalid schema: missing 'jurisdictions' key.")

    return data

def classify_use_case(system_description: Dict[str, Any], rules: Dict[str, Any]) -> Dict[str, Any]:
    """
    Maps a described AI use-case to risk tiers and themes based on the rules.
    """
    classification = {}
    regions = system_description.get("deployment_region", [])

    for region in regions:
        if region in rules["jurisdictions"]:
            region_rules = rules["jurisdictions"][region]
            classification[region] = {"tier": None, "theme": None}

            # EU Risk Tiers
            if "risk_tiers" in region_rules:
                for tier in region_rules["risk_tiers"]:
                    # Match conditions
                    match = False
                    if not tier["conditions"]: # Catch-all
                        match = True
                    for condition in tier["conditions"]:
                        if system_description.get(condition["key"]) == condition["value"]:
                            match = True
                            break
                    if match:
                        classification[region]["tier"] = tier["tier"]
                        break # Prioritize higher tiers if ordered that way

            # US Themes
            if "themes" in region_rules:
                classification[region]["theme"] = []
                for theme in region_rules["themes"]:
                    match = False
                    if not theme["conditions"]:
                        match = True
                    for condition in theme["conditions"]:
                        if system_description.get(condition["key"]) == condition["value"]:
                            match = True
                            break
                    if match:
                        classification[region]["theme"].append(theme["theme"])

    return classification

def get_obligations(system_description: Dict[str, Any], rules: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Lists required obligations and documentation for the system.
    """
    obligations = {}
    regions = system_description.get("deployment_region", [])

    for region in regions:
        if region in rules["jurisdictions"]:
            region_rules = rules["jurisdictions"][region]
            obligations[region] = []

            if "risk_tiers" in region_rules:
                for tier in region_rules["risk_tiers"]:
                    match = False
                    if not tier["conditions"]:
                        match = True
                    for condition in tier["conditions"]:
                        if system_description.get(condition["key"]) == condition["value"]:
                            match = True
                            break
                    if match:
                        obligations[region].extend(tier["obligations"])
                        break

            if "themes" in region_rules:
                for theme in region_rules["themes"]:
                    match = False
                    if not theme["conditions"]:
                        match = True
                    for condition in theme["conditions"]:
                        if system_description.get(condition["key"]) == condition["value"]:
                            match = True
                            break
                    if match:
                        obligations[region].extend(theme["obligations"])

    return obligations
