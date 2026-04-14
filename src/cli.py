"""
CLI Interface for the AI Economic Impact Dashboard.
"""
import argparse
import sys
import json
from src.data.hardware import get_available_hardware, REGIONAL_PRICING_MULTIPLIERS
from src.models.compute import calculate_training_cost
from src.visualization.plots import plot_cost_projections, plot_cost_per_parameter, plot_regional_comparisons

def main():
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(description="AI Economic Impact Dashboard - Compute Cost Estimator")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Estimate command
    estimate_parser = subparsers.add_parser("estimate", help="Estimate training cost for a model")
    estimate_parser.add_argument("--params", type=float, required=True, help="Number of parameters in billions")
    estimate_parser.add_argument("--tokens", type=float, required=True, help="Number of training tokens in billions")
    estimate_parser.add_argument("--hardware", type=str, default="H100_80GB", choices=get_available_hardware(), help="Hardware type to use")
    estimate_parser.add_argument("--env", type=str, default="cloud", choices=["cloud", "on_premise"], help="Environment (cloud or on_premise)")
    estimate_parser.add_argument("--region", type=str, default="US_EAST", choices=list(REGIONAL_PRICING_MULTIPLIERS.keys()), help="Region for pricing")
    estimate_parser.add_argument("--utilization", type=float, default=0.4, help="Hardware Model FLOPs Utilization (MFU) rate")
    estimate_parser.add_argument("--json", action="store_true", help="Output result as JSON")

    # Visualize command
    viz_parser = subparsers.add_parser("visualize", help="Generate interactive visualizations")
    viz_parser.add_argument("--all", action="store_true", help="Generate all visualizations")

    args = parser.parse_args()

    if args.command == "estimate":
        try:
            result = calculate_training_cost(
                params_b=args.params,
                tokens_b=args.tokens,
                hardware_name=args.hardware,
                environment=args.env,
                region=args.region,
                utilization_rate=args.utilization
            )

            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print("\n=== Training Cost Estimate ===")
                print(f"Model Size: {args.params}B params")
                print(f"Training Tokens: {args.tokens}B tokens")
                print(f"Hardware: {args.hardware} ({args.env}, {args.region})")
                print(f"Utilization: {args.utilization*100}%")
                print("-" * 30)
                print(f"Total FLOPs: {result['total_flops']:.2e}")
                print(f"Total Time: {result['total_time_hours']:.1f} hours ({result['total_time_days']:.1f} days)")
                print(f"Hourly Cost: ${result['hourly_cost']:.2f}")
                print(f"Total Cost: ${result['total_cost']:,.2f}")
                print("==============================\n")

        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "visualize":
        print("Generating visualizations...")
        f1 = plot_cost_projections()
        print(f"Created: {f1}")
        f2 = plot_cost_per_parameter()
        print(f"Created: {f2}")
        f3 = plot_regional_comparisons()
        print(f"Created: {f3}")
        print("Done.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
