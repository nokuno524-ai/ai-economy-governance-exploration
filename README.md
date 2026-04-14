# AI Economic Impact Dashboard

This repository explores the economic impact of AI and governance frameworks. It includes a compute cost estimator prototype tool for modeling AI training costs.

## Features

- **Compute Cost Estimator:** Models AI training costs based on parameters (model size, training tokens, hardware type, cloud vs on-premise, utilization rate).
- **Interactive Visualizations:** Generates Plotly visualizations showing cost projections over time, cost-per-parameter scaling, and regional cost comparisons.
- **Historical Data:** Includes historical data points for model sizes, tokens, and estimated training costs.

## Setup

1. Clone the repository.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

The main CLI application can be executed from the project root using:

```bash
PYTHONPATH=. python3 src/cli.py [command]
```

### Estimate Command

Estimate the training cost for a specific model configuration:

```bash
PYTHONPATH=. python3 src/cli.py estimate --params 70 --tokens 15000 --hardware H100_80GB
```

**Options:**
- `--params`: Number of parameters in billions (required).
- `--tokens`: Number of training tokens in billions (required).
- `--hardware`: Hardware type to use (e.g., `A100_80GB`, `H100_80GB`, `B200`).
- `--env`: Environment (`cloud` or `on_premise`).
- `--region`: Region for pricing (e.g., `US_EAST`, `EU_WEST`).
- `--utilization`: Hardware Model FLOPs Utilization (MFU) rate.
- `--json`: Output the result as JSON.

### Visualize Command

Generate interactive Plotly visualizations:

```bash
PYTHONPATH=. python3 src/cli.py visualize
```

Visualizations are saved as interactive HTML files in the `output/` directory:
- `cost_projections.html`: Historical AI model training costs over time.
- `cost_per_parameter.html`: Cost scaling by parameter size.
- `regional_comparison.html`: Regional training cost comparison.

## Testing

The project uses `pytest` for testing. Run the test suite from the project root:

```bash
PYTHONPATH=. pytest tests/
```

## Project Structure

- `src/data/`: Hardware configuration, regional pricing, and historical model data.
- `src/models/`: Compute cost calculation logic.
- `src/visualization/`: Plotly visualization functions.
- `src/api/`: Mock API client for fetching live pricing data.
- `src/cli.py`: Command-line interface entry point.
- `tests/`: Pytest unit and integration tests.
- `output/`: Directory where generated HTML visualizations are saved.
