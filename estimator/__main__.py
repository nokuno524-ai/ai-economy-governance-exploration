"""
CLI entry point for the estimator package.
"""

import argparse
import json
import csv
import sys
from typing import Any

from estimator.compute_cost import estimate_training_cost, estimate_inference_cost, amortize
from estimator.task_exposure import load_tasks_data, rank_occupations, aggregate_sector_exposure


def output_result(data: Any, format_type: str) -> None:
    """Format and print the result based on the requested format."""
    if format_type == "json":
        print(json.dumps(data, indent=2))
    elif format_type == "csv":
        writer = csv.writer(sys.stdout)
        if isinstance(data, dict):
            # For simple dictionaries
            writer.writerow(data.keys())
            writer.writerow(data.values())
        elif isinstance(data, list) and all(isinstance(x, tuple) for x in data):
            # For lists of tuples (e.g., occupation rankings)
            writer.writerow(["Key", "Value"])
            writer.writerows(data)
        else:
            print(f"Unsupported data type for CSV: {type(data)}")
    elif format_type == "markdown":
        if isinstance(data, dict):
            print("| Key | Value |")
            print("|---|---|")
            for k, v in data.items():
                print(f"| {k} | {v} |")
        elif isinstance(data, list) and all(isinstance(x, tuple) for x in data):
            print("| Key | Value |")
            print("|---|---|")
            for k, v in data:
                print(f"| {k} | {v:.4f} |")
        else:
            print(f"Unsupported data type for Markdown: {type(data)}")
    else:
        print(data)


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="AI Economic Impact Estimator CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Output format arguments
    format_parser = argparse.ArgumentParser(add_help=False)
    format_group = format_parser.add_mutually_exclusive_group()
    format_group.add_argument("--json", action="store_true", help="Output in JSON format")
    format_group.add_argument("--csv", action="store_true", help="Output in CSV format")
    format_group.add_argument("--markdown", action="store_true", help="Output in Markdown format")

    # Training subcommand
    parser_training = subparsers.add_parser("training", parents=[format_parser], help="Estimate training cost")
    parser_training.add_argument("--gpus", type=int, required=True, help="Number of GPUs")
    parser_training.add_argument("--hours", type=float, required=True, help="Total hours of training")
    parser_training.add_argument("--gpu-type", type=str, default="a100", help="GPU type (a100, h100)")
    parser_training.add_argument("--utilization", type=float, default=1.0, help="GPU utilization (0.0 to 1.0)")
    parser_training.add_argument("--amortize-months", type=int, default=None, help="Amortize total cost over N months")

    # Inference subcommand
    parser_inference = subparsers.add_parser("inference", parents=[format_parser], help="Estimate inference cost")
    parser_inference.add_argument("--tokens-in", type=int, required=True, help="Input tokens")
    parser_inference.add_argument("--tokens-out", type=int, required=True, help="Output tokens")
    parser_inference.add_argument("--model-class", type=str, default="mid", help="Model class (small, mid, large)")

    # Exposure subcommand
    parser_exposure = subparsers.add_parser("exposure", parents=[format_parser], help="Analyze task exposure")
    parser_exposure.add_argument("--level", type=str, choices=["occupation", "sector"], default="occupation", help="Aggregation level")

    args = parser.parse_args()

    format_type = "json"
    if args.csv:
        format_type = "csv"
    elif args.markdown:
        format_type = "markdown"

    try:
        if args.command == "training":
            res = estimate_training_cost(args.gpus, args.hours, args.gpu_type, args.utilization)
            if args.amortize_months:
                res["amortized_low_cost"] = amortize(res["low_cost"], args.amortize_months)
                res["amortized_high_cost"] = amortize(res["high_cost"], args.amortize_months)
            output_result(res, format_type)
        elif args.command == "inference":
            res = estimate_inference_cost(args.tokens_in, args.tokens_out, args.model_class)
            output_result(res, format_type)
        elif args.command == "exposure":
            data = load_tasks_data()
            if args.level == "occupation":
                res = rank_occupations(data)
                output_result(res, format_type)
            elif args.level == "sector":
                res = aggregate_sector_exposure(data)
                output_result(res, format_type)
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
