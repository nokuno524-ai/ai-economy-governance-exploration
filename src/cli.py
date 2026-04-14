"""
AI Economic Impact Dashboard CLI

Command-line interface to access compute cost estimation, task exposure analysis,
and governance timeline visualizations.
"""
import argparse
import sys
import json
from src.analyzers.compute_cost import estimate_training_cost, project_inference_cost, compare_tco
from src.analyzers.task_exposure import get_industry_exposure_data, analyze_exposure_by_type
from src.governance.compliance import get_compliance_timeline
from src.visualizations.plots import plot_cost_projections, plot_task_exposure_heatmap, plot_governance_timeline

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="AI Economic Impact Dashboard CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Compute Cost Estimator
    compute_parser = subparsers.add_parser("compute", help="Estimate compute costs")
    compute_subparsers = compute_parser.add_subparsers(dest="compute_command", help="Compute commands")

    training_parser = compute_subparsers.add_parser("training", help="Estimate training cost")
    training_parser.add_argument("--params", type=float, required=True, help="Parameters in billions")
    training_parser.add_argument("--tokens", type=float, required=True, help="Tokens in trillions")

    inference_parser = compute_subparsers.add_parser("inference", help="Project inference costs")
    inference_parser.add_argument("--current-cost", type=float, required=True, help="Current cost per 1M tokens")
    inference_parser.add_argument("--years", type=int, default=5, help="Years to project (default: 5)")

    tco_parser = compute_subparsers.add_parser("tco", help="Compare total cost of ownership")
    tco_parser.add_argument("--tokens-monthly", type=float, required=True, help="Expected monthly tokens in millions")
    tco_parser.add_argument("--api-cost", type=float, required=True, help="Cloud API cost per 1M tokens")
    tco_parser.add_argument("--hardware-monthly", type=float, required=True, help="Monthly cost for self-hosted hardware")
    tco_parser.add_argument("--ops-monthly", type=float, required=True, help="Monthly operational cost for self-hosting")
    tco_parser.add_argument("--hybrid-percent", type=float, default=0.2, help="Fraction of tokens handled by API in hybrid setup (0.0 - 1.0)")

    # Visualizations
    viz_parser = subparsers.add_parser("visualize", help="Generate dashboard visualizations")
    viz_parser.add_argument("--all", action="store_true", help="Generate all visualizations")

    args = parser.parse_args()

    if args.command == "compute":
        if args.compute_command == "training":
             res = estimate_training_cost(args.params, args.tokens)
             print(json.dumps(res, indent=2))
        elif args.compute_command == "inference":
             res = project_inference_cost(args.current_cost, args.years)
             print(json.dumps(res, indent=2))
        elif args.compute_command == "tco":
             res = compare_tco(args.tokens_monthly, args.api_cost, args.hardware_monthly, args.ops_monthly, args.hybrid_percent)
             print(json.dumps(res, indent=2))
        else:
             compute_parser.print_help()
    elif args.command == "visualize":
        print("Generating visualizations...")

        # 1. Cost Projection
        projections = project_inference_cost(0.48, 5) # Default baseline
        plot_cost_projections(projections)
        print("Created cost projection plot: output/cost_projection.html")

        # 2. Task Exposure
        exposure_df = get_industry_exposure_data()
        plot_task_exposure_heatmap(exposure_df)
        print("Created task exposure heatmap: output/task_exposure.html")

        # 3. Governance Timeline
        timeline_df = get_compliance_timeline()
        plot_governance_timeline(timeline_df)
        print("Created governance timeline: output/governance_timeline.html")

        print("Done.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
