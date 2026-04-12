# AI Economy Impact & Governance Exploration

This project explores AI's economic impact and governance frameworks from a computer science perspective. It includes an 'AI Economic Impact Dashboard' which acts as a compute cost estimator, a task exposure analyzer, and a governance compliance engine.

## Overview
- **Productivity Gains:** Tools to measure and correlate productivity impacts of AI.
- **Labor Market Shifts:** Analysis tools to see what tasks and industries are exposed to AI augmentation/automation.
- **Compute Economics:** Tools estimating training costs, projecting inference cost drops ("LLMflation"), and calculating Total Cost of Ownership (TCO).
- **Governance Frameworks:** Compliance timelines checking AI milestones against regulations like the EU AI Act and US Executive Orders.

## Project Structure
- `src/analyzers/`: Logic for estimating compute costs and mock data for task exposures.
- `src/governance/`: Mock timelines for governance compliance.
- `src/visualizations/`: Matplotlib and Plotly logic to graph cost drops, exposure heatmaps, and governance timelines.
- `src/cli.py`: Command-Line Interface to easily use all tools.

## Installation
1. Clone the repository.
2. Install dependencies via `pip install -r requirements.txt`. This will install `pytest`, `matplotlib`, `plotly`, `pandas`, and `kaleido`.

## Tool Usage
Run the CLI tool from the root directory:
- To estimate AI model training cost: `PYTHONPATH=. python3 src/cli.py compute training --params <billions> --tokens <trillions>`
- To project inference cost drop: `PYTHONPATH=. python3 src/cli.py compute inference --current-cost <cost_per_million_tokens> --years <num_years>`
- To compare total cost of ownership (TCO): `PYTHONPATH=. python3 src/cli.py compute tco --tokens-monthly <millions> --api-cost <cost> --hardware-monthly <cost> --ops-monthly <cost>`
- To generate visualizations (cost projection, task exposure, governance timeline): `PYTHONPATH=. python3 src/cli.py visualize --all`
  - Output files are saved interactively as `.html` files in the `output/` directory.

## Methodology & Data Sources
- Training compute estimations are based on the approximation `6 * params * tokens` for FLOPs.
- Inference projections use historical trends of a 10x cost reduction per year.
- Data sources mock O*NET for task exposure and synthesize real-world regulatory milestones (EU AI Act, US EOs).

See `RESEARCH.md` for full detailed background research and paper references.
