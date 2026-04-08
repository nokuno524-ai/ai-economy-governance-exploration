# AI Economy Impact & Governance: A CS Researcher's Exploration

**Date:** 2026-04-08
**Status:** ✅ Explored
**Focus:** Economic impact of AI + AI governance frameworks through a computer science lens

---

## 1. Summary of Key Research Areas & Findings

### 1.1 AI Productivity Gains

**Key Paper: Brynjolfsson, Li & Raymond (2023) — "Generative AI at Work" (NBER w31161)**
- Studied 5,179 customer support agents with staggered AI tool introduction
- **14% average productivity increase** (issues resolved per hour)
- **34% improvement for novice/low-skilled workers**, minimal for experienced
- AI disseminates best practices from high-performing workers → compresses experience curve
- Also improved customer sentiment and employee retention
- **CS angle:** The heterogeneity of effects suggests AI acts as a knowledge transfer mechanism, not just automation — this is a systems modeling problem

**Broader productivity landscape (2024-2026):**
- McKinsey estimates generative AI could add $2.6-4.4 trillion annually to global GDP
- Stanford HAI 2025 AI Index tracks comprehensive metrics on AI capabilities vs. economic impact
- Key gap: **real-time, granular productivity measurement** — most studies are retroactive
- CS opportunity: Build instrumentation/observability tools for AI-augmented workflows

### 1.2 Labor Market Shifts

**Key findings from literature:**
- Acemoglu (2024, MIT) argues macroeconomic productivity gains from AI are likely modest (0.5-1% over 10 years) absent new tasks creation
- The "task-based" framework (Autor, Acemoglu, Restrepo) remains dominant: AI automates tasks, not jobs
- Occupations most exposed: knowledge work (legal, financial analysis, coding, writing)
- Least exposed: physical/manual labor (plumbing, construction, nursing)
- **CS angle:** Granular task-level datasets (O*NET, BLS) need systematic mapping to AI capabilities

**Critical gap:** No standardized benchmark maps AI model capabilities to specific occupational tasks at scale. Most studies use coarse exposure classifications.

### 1.3 Compute Economics

**Training costs (frontier models):**
- GPT-4: $78-100M estimated training cost
- Gemini Ultra 1.0: ~$192M
- Frontier 2025-2026: projected $5-10B
- Training compute doubles every ~9 months for largest runs

**Training costs (smaller models):**
- 1B params: $2K-$15K
- 7B params: $50K-$500K  
- 70B params: $1.2M-$6M
- 40-60% reduction vs 2023 due to algorithmic + hardware improvements

**Inference costs — the "LLMflation" phenomenon (a16z, 2024):**
- LLM inference cost for equivalent performance drops **10x per year**
- GPT-3.5-level performance: $60/M tokens (2021) → $0.06/M tokens (2024) = **1000x in 3 years**
- GPT-4-level performance: $30/M tokens (Mar 2023) → ~$0.48/M tokens = **62x in <2 years**
- **Key drivers:** better GPUs, quantization (16→4 bit = 4x), software optimizations, smaller models trained on more tokens, open-source competition
- But total inference spend is *rising* due to usage explosion → inference market projected $106B (2025) → $255B (2030)

**Training data costs (arxiv 2504.12427):**
- Paper argues training data labor cost is 10-1000x the compute cost for training
- Studied 64 LLMs (2016-2024), estimated cost of paying humans to produce training data from scratch
- Major unpriced externality: trillions of words from books, papers, code, social media
- **CS angle:** Data valuation frameworks, provenance tracking, compensation mechanisms

### 1.4 AI Governance Frameworks

**EU AI Act (effective August 1, 2024):**
- Risk-based classification: unacceptable → high → limited → minimal risk
- Prohibitions effective Feb 2025 (social scoring, manipulative AI, real-time biometric ID)
- GPAI model governance rules effective Aug 2025
- High-risk AI full compliance by Aug 2026-2027
- Fines up to €35M or 7% global turnover
- **CS gap:** Automated compliance checking tools; risk classification benchmarks

**US Federal Approach (2025-2026):**
- Jan 2025: EO 14179 "Removing Barriers to American Leadership in AI" — deregulatory stance
- Jul 2025: AI Action Plan — focus on exports, data center infrastructure, preventing "woke AI"
- Dec 2025: EO 14365 — preempts state AI laws deemed "onerous"; DOJ AI Litigation Task Force
- Mar 2026: Commerce Dept to evaluate state AI laws
- **Key tension:** Federal preemption vs state-level consumer protection (CO, CA, IL have their own laws)

**China:**
- Algorithmic recommendation regulations (2022), deep synthesis rules (2023), generative AI measures (2023)
- Focus on content control + social stability, not individual rights
- Mandatory algorithmic audits for public-facing systems
- **CS gap:** Cross-jurisdictional compliance comparison tools

---

## 2. Data Sources Available

### Public Datasets & APIs
| Source | Data | Access |
|--------|------|--------|
| BLS (Bureau of Labor Statistics) | Employment, wages, occupational data | Free API |
| O*NET | Occupational task/skill taxonomies | Free download |
| OECD AI Policy Observatory | National AI strategies, policy comparisons | Free |
| World Bank Open Data | GDP, employment, technology indicators | Free API |
| Stanford HAI AI Index | Comprehensive AI metrics | Annual report + data |
| Epoch AI | Training compute, cost estimates for ML models | Free |
| Hugging Face Open LLM Leaderboard | Model performance benchmarks | Free API |
| arxiv | AI research papers | Free API |
| SEC EDGAR | Corporate AI investment disclosures | Free API |

### Commercial/Paid Sources
- McKinsey, BCG reports (PDF)
- CB Insights, PitchBook (startup/investment data)
- SemiAnalysis (chip/compute market analysis)

---

## 3. Proposed Framework: AI Economic Impact Dashboard

### Concept
A Python tool that **automatically aggregates and correlates** public economic indicators with AI capability metrics to identify:
1. Which occupations/sectors are most exposed to AI automation
2. How compute costs track against productivity measures
3. Regulatory compliance burden across jurisdictions

### Architecture
```
ai-economy-governance/
├── src/
│   ├── collectors/       # API clients for BLS, OECD, World Bank, arxiv
│   ├── analyzers/        # Task exposure scoring, compute cost modeling
│   ├── governance/       # Regulatory framework comparison engine
│   └── models/           # Data models and schemas
├── data/
│   ├── raw/              # Cached API responses
│   └── processed/        # Cleaned/normalized datasets
├── notebooks/            # Analysis notebooks
├── tests/
└── output/               # Generated reports, visualizations
```

### Core Prototype: Compute Cost Estimator
Given the richness of compute economics data, the most tractable prototype is a **compute cost estimator** that:
- Takes model parameters, training tokens, and target hardware as input
- Estimates training cost, inference cost per token, and total cost of ownership
- Compares across GPU generations (A100, H100, B200)
- Models inference scaling (users, queries/day, context length)
- Projects future costs based on historical trends

---

## 4. Novelty Assessment

### What's genuinely new here:
1. **Unified compute + labor economics model** — most work treats these separately; a tool linking training costs → deployment costs → labor displacement would be novel
2. **Real-time regulatory compliance scoring** — automated comparison of AI system properties against multi-jurisdiction requirements
3. **Benchmark-to-occupation mapping** — systematic mapping from AI benchmark performance to occupational task capability

### What's incremental:
- Simple compute cost calculators exist (e.g., various blog posts)
- Individual API clients for BLS/OECD exist
- Governance comparison matrices exist in PDF form

### The CS researcher's unique contribution:
- **Building tools and infrastructure** that economists/policymakers lack the technical skills to create
- **Formal models** of compute scaling that capture the interplay of hardware, algorithms, and data
- **Automated analysis pipelines** that can process regulatory text → structured compliance requirements

---

## 5. Experiment Plan

### Phase 1: Compute Cost Estimator (Prototype — this session)
- [x] Build Python CLI tool for estimating AI model training and inference costs
- [x] Parameterized model: params, tokens, hardware, utilization
- [x] Historical cost tracking (inference price normalization)
- [x] Multi-GPU comparison (A100 vs H100 vs B200)
- [x] Output: cost breakdown, scaling projections

### Phase 2: Task Exposure Analyzer (future)
- [ ] Load O*NET task/skill data
- [ ] Map AI benchmark performance (MMLU, HumanEval, etc.) to task capabilities
- [ ] Score occupations by AI exposure level
- [ ] Compare with BLS employment data

### Phase 3: Governance Compliance Engine (future)
- [ ] Parse regulatory texts (EU AI Act, US EOs)
- [ ] Extract structured requirements (data handling, transparency, auditing)
- [ ] Given an AI system description, generate compliance checklist
- [ ] Cross-jurisdiction comparison matrix

---

## 6. Key References

1. Brynjolfsson, Li & Raymond (2023). "Generative AI at Work." NBER w31161.
2. Kandpal et al. (2025). "The Most Expensive Part of an LLM should be its Training Data." arxiv 2504.12427.
3. a16z (2024). "LLMflation — LLM inference cost is going down fast."
4. Stanford HAI (2025). "AI Index Report 2025."
5. EU AI Act (2024). Regulation (EU) 2024/1689.
6. US Executive Order 14365 (Dec 2025). "Ensuring a National Policy Framework for AI."
7. US Executive Order 14179 (Jan 2025). "Removing Barriers to American Leadership in AI."
8. Acemoglu (2024). "The Simple Macroeconomics of AI." NBER.
9. Epoch AI. Training compute and cost trend data.
10. McKinsey (2023). "The Economic Potential of Generative AI."
