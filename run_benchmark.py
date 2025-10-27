#!/usr/bin/env python3
"""
Simple benchmark runner script for the FastAPI microservice.
"""
import subprocess
import sys
import os
import argparse
from pathlib import Path


def run_benchmark(url: str, category: str = None, output: str = None, auth_token: str = None, webhook_auth_token: str = None):
    """Run benchmark with given parameters."""
    print("FastAPI Microservice Benchmark Runner")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Error: pyproject.toml not found. Please run from project root.")
        sys.exit(1)
    
    # Check if uv is available
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: uv not found. Please install uv first.")
        sys.exit(1)
    
    # Build command
    command = ["uv", "run", "python", "benchmark/benchmark.py", "--url", url]
    
    if category:
        command.extend(["--category", category])
    
    if output:
        command.extend(["--output", output])
    
    if auth_token:
        command.extend(["--auth-token", auth_token])
    
    if webhook_auth_token:
        command.extend(["--webhook-auth-token", webhook_auth_token])
    
    print(f"Running benchmark against: {url}")
    if category:
        print(f"Category: {category}")
    if output:
        print(f"Output file: {output}")
    print("=" * 50)
    
    try:
        result = subprocess.run(command, check=True)
        print("✅ Benchmark completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Benchmark failed with exit code {e.returncode}")
        return False
    except KeyboardInterrupt:
        print("\n❌ Benchmark interrupted by user")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run FastAPI microservice benchmark")
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Base URL of the FastAPI server (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--category",
        choices=["health", "operations", "step", "example", "errors", "performance", "edge"],
        help="Run specific category of tests (default: all tests)"
    )
    parser.add_argument(
        "--output",
        help="Path to save results JSON file (optional)"
    )
    parser.add_argument(
        "--auth-token",
        default=os.getenv("AUTH_TOKEN"),
        help="Authentication token (default: from AUTH_TOKEN env var)"
    )
    parser.add_argument(
        "--webhook-auth-token",
        default=os.getenv("WEBHOOK_AUTH_TOKEN"),
        help="Webhook authentication token (default: from WEBHOOK_AUTH_TOKEN env var)"
    )
    
    args = parser.parse_args()
    
    success = run_benchmark(
        url=args.url,
        category=args.category,
        output=args.output,
        auth_token=args.auth_token,
        webhook_auth_token=args.webhook_auth_token
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
