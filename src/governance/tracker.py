from dataclasses import dataclass, field
from typing import List, Dict, Any, Set

@dataclass
class AIRegulation:
    """
    Schema for AI regulations.
    """
    id: str
    name: str
    jurisdiction: str
    scope: List[str]
    enforcement: str
    compliance_requirements: List[str]

# Curated dataset of 20+ real AI regulations
REGULATIONS_DATA = [
    AIRegulation(
        id="eu_ai_act",
        name="EU AI Act",
        jurisdiction="European Union",
        scope=["High-risk AI systems", "GPAI models", "Prohibited AI systems", "Limited risk AI systems"],
        enforcement="National competent authorities and EU AI Office",
        compliance_requirements=["Conformity assessments", "CE marking", "Quality management system", "Post-market monitoring", "Transparency requirements"]
    ),
    AIRegulation(
        id="us_eo_14110",
        name="US Executive Order 14110 on Safe, Secure, and Trustworthy AI",
        jurisdiction="United States (Federal)",
        scope=["Dual-use foundation models", "Federal agencies using AI"],
        enforcement="Federal agencies (NIST, DoC, etc.)",
        compliance_requirements=["Red-teaming tests reporting", "Safety evaluations", "Watermarking guidance adoption"]
    ),
    AIRegulation(
        id="china_generative_ai_measures",
        name="Interim Measures for the Management of Generative AI Services",
        jurisdiction="China",
        scope=["Generative AI services provided to the public in China"],
        enforcement="Cyberspace Administration of China (CAC)",
        compliance_requirements=["Security assessment", "Algorithm filing", "Content filtering", "User identity verification"]
    ),
    AIRegulation(
        id="canada_aida",
        name="Artificial Intelligence and Data Act (AIDA)",
        jurisdiction="Canada",
        scope=["High-impact AI systems"],
        enforcement="Minister of Innovation, Science and Industry",
        compliance_requirements=["Assess and mitigate risks of harm or biased output", "Proportionate risk management", "Plain language public reporting"]
    ),
    AIRegulation(
        id="uk_ai_white_paper",
        name="UK AI Regulation White Paper (Pro-innovation approach)",
        jurisdiction="United Kingdom",
        scope=["All AI systems (context-specific)"],
        enforcement="Existing sectoral regulators (e.g., ICO, CMA)",
        compliance_requirements=["Safety, security, and robustness", "Appropriate transparency and explainability", "Fairness", "Accountability and governance", "Contestability and redress"]
    ),
    AIRegulation(
        id="colorado_sb24_205",
        name="Colorado Artificial Intelligence Act (SB24-205)",
        jurisdiction="Colorado (US State)",
        scope=["High-risk AI systems making consequential decisions"],
        enforcement="Colorado Attorney General",
        compliance_requirements=["Developer risk management policy", "Impact assessments", "Consumer notification", "Right to correct"]
    ),
    AIRegulation(
        id="california_ab_2013",
        name="California AB 2013: Generative AI Training Data Transparency",
        jurisdiction="California (US State)",
        scope=["Generative AI systems"],
        enforcement="California State Attorney General",
        compliance_requirements=["Publish high-level summary of training datasets", "Disclose whether data included copyrighted materials or personal information"]
    ),
    AIRegulation(
        id="utah_sb_149",
        name="Utah AI Policy Act (SB 149)",
        jurisdiction="Utah (US State)",
        scope=["Generative AI systems interacting with users"],
        enforcement="Utah Department of Commerce / Attorney General",
        compliance_requirements=["Clear and conspicuous disclosure of AI interaction (if asked)", "Regulated occupations must affirmatively disclose AI use"]
    ),
    AIRegulation(
        id="eu_gdpr_ai",
        name="General Data Protection Regulation (GDPR) - Automated Decision Making",
        jurisdiction="European Union",
        scope=["AI systems processing personal data for automated decision making"],
        enforcement="Data Protection Authorities (DPAs)",
        compliance_requirements=["Right not to be subject to solely automated decision-making", "Right to explanation", "Data Protection Impact Assessment (DPIA)"]
    ),
    AIRegulation(
        id="us_blueprint_ai_bor",
        name="Blueprint for an AI Bill of Rights",
        jurisdiction="United States (Federal, Advisory)",
        scope=["Automated systems that meaningfully impact the public's rights, opportunities, or access"],
        enforcement="None (Advisory, guiding agency actions)",
        compliance_requirements=["Safe and effective systems", "Algorithmic discrimination protections", "Data privacy", "Notice and explanation", "Human alternatives, consideration, and fallback"]
    ),
    AIRegulation(
        id="brazil_pl_2338",
        name="Brazil AI Bill (PL 2338/2023)",
        jurisdiction="Brazil",
        scope=["High-risk and excessive-risk AI systems"],
        enforcement="To be determined competent authority",
        compliance_requirements=["Algorithmic impact assessment", "Transparency", "Human oversight", "Strict liability for high-risk systems"]
    ),
    AIRegulation(
        id="singapore_model_ai_gov_framework",
        name="Model AI Governance Framework",
        jurisdiction="Singapore",
        scope=["Organizations deploying AI solutions"],
        enforcement="None (Voluntary framework)",
        compliance_requirements=["Internal governance structures", "Determining level of human involvement", "Operations management", "Stakeholder interaction and communication"]
    ),
    AIRegulation(
        id="japan_ai_guidelines",
        name="AI Guidelines for Business",
        jurisdiction="Japan",
        scope=["AI developers, providers, and business users"],
        enforcement="None (Soft law approach)",
        compliance_requirements=["Human-centric AI", "Safety", "Fairness", "Privacy protection", "Security", "Transparency", "Accountability"]
    ),
    AIRegulation(
        id="south_korea_ai_act",
        name="Framework Act on Artificial Intelligence (Pending)",
        jurisdiction="South Korea",
        scope=["High-risk AI systems"],
        enforcement="Ministry of Science and ICT",
        compliance_requirements=["Prior notification for high-risk systems", "Ensuring user trust", "Fostering AI industry"]
    ),
    AIRegulation(
        id="australia_safe_ai_framework",
        name="Safe and Responsible AI in Australia",
        jurisdiction="Australia",
        scope=["High-risk AI settings"],
        enforcement="Sector-specific regulators (proposed)",
        compliance_requirements=["Mandatory guardrails for high-risk AI", "Testing and certification", "Transparency obligations"]
    ),
    AIRegulation(
        id="council_of_europe_ai_treaty",
        name="Framework Convention on AI, Human Rights, Democracy, and the Rule of Law",
        jurisdiction="International (Council of Europe + signatories)",
        scope=["AI systems impacting human rights, democracy, and rule of law"],
        enforcement="Varies by signatory state",
        compliance_requirements=["Protect human rights", "Ensure democratic processes", "Maintain rule of law", "Transparency and oversight mechanisms"]
    ),
    AIRegulation(
        id="unesco_ai_ethics",
        name="Recommendation on the Ethics of Artificial Intelligence",
        jurisdiction="International (UNESCO)",
        scope=["Global AI lifecycle"],
        enforcement="None (Normative framework)",
        compliance_requirements=["Proportionality", "Safety and security", "Right to privacy", "Multi-stakeholder governance", "Environmental sustainability"]
    ),
    AIRegulation(
        id="nyc_local_law_144",
        name="NYC Local Law 144 (Automated Employment Decision Tools)",
        jurisdiction="New York City (Local)",
        scope=["Automated employment decision tools (AEDTs)"],
        enforcement="NYC Department of Consumer and Worker Protection (DCWP)",
        compliance_requirements=["Independent bias audit", "Public summary of audit results", "Notice to candidates"]
    ),
    AIRegulation(
        id="taiwan_ai_basic_law",
        name="Draft AI Basic Law",
        jurisdiction="Taiwan",
        scope=["Government and industry AI use"],
        enforcement="National Science and Technology Council (NSTC)",
        compliance_requirements=["Privacy protection", "Information security", "Transparency", "Risk management"]
    ),
    AIRegulation(
        id="g7_hiroshima_process",
        name="G7 Hiroshima AI Process Comprehensive Policy Framework",
        jurisdiction="International (G7)",
        scope=["Advanced AI systems (e.g., foundation models)"],
        enforcement="None (Voluntary code of conduct)",
        compliance_requirements=["Identify and mitigate risks", "Report vulnerabilities", "Information sharing", "Implement watermarking/provenance"]
    ),
    AIRegulation(
        id="india_dpdp_act",
        name="Digital Personal Data Protection Act (DPDP Act) - AI Implications",
        jurisdiction="India",
        scope=["Processing of digital personal data (including by AI)"],
        enforcement="Data Protection Board of India",
        compliance_requirements=["Consent for data processing", "Purpose limitation", "Data minimization", "Right to information"]
    )
]

def get_regulations() -> List[AIRegulation]:
    """Returns all available regulations."""
    return REGULATIONS_DATA

def get_regulation(reg_id: str) -> AIRegulation:
    """
    Fetches a specific regulation by ID.

    Args:
        reg_id: The ID of the regulation to fetch.

    Returns:
        The AIRegulation object if found.

    Raises:
        ValueError: If the regulation ID is not found.
    """
    for reg in REGULATIONS_DATA:
        if reg.id == reg_id:
            return reg
    raise ValueError(f"Regulation with ID '{reg_id}' not found.")

def compare_regulations(regulation_ids: List[str]) -> Dict[str, Any]:
    """
    Analyzes regulatory overlap and gaps between specified regulations.

    Args:
        regulation_ids: A list of regulation IDs to compare.

    Returns:
        A dictionary containing comparative analysis:
        - 'overlaps': Scope items common to all selected regulations.
        - 'gaps': Requirements present in some but not all selected regulations.
        - 'all_scopes': Union of all scopes.
        - 'all_requirements': Union of all compliance requirements.
    """
    if not regulation_ids:
        return {"overlaps": set(), "gaps": set(), "all_scopes": set(), "all_requirements": set()}

    regs = [get_regulation(rid) for rid in regulation_ids]

    # Calculate scopes overlap (intersection)
    scopes_list = [set(reg.scope) for reg in regs]
    overlaps = set.intersection(*scopes_list) if scopes_list else set()

    # Calculate union of scopes
    all_scopes = set.union(*scopes_list) if scopes_list else set()

    # Calculate requirements union
    reqs_list = [set(reg.compliance_requirements) for reg in regs]
    all_requirements = set.union(*reqs_list) if reqs_list else set()

    # Calculate requirements intersection
    common_requirements = set.intersection(*reqs_list) if reqs_list else set()

    # Gaps are requirements not shared by all (union - intersection)
    gaps = all_requirements - common_requirements

    return {
        "overlaps": overlaps,
        "gaps": gaps,
        "all_scopes": all_scopes,
        "all_requirements": all_requirements,
        "common_requirements": common_requirements
    }

def generate_compliance_checklist(regulation_ids: List[str]) -> Dict[str, List[str]]:
    """
    Generates a grouped compliance checklist across selected regulations.

    Args:
        regulation_ids: A list of regulation IDs to include in the checklist.

    Returns:
        A dictionary mapping regulation names to their respective list of compliance requirements.
    """
    checklist = {}
    for rid in regulation_ids:
        reg = get_regulation(rid)
        checklist[reg.name] = reg.compliance_requirements

    return checklist
