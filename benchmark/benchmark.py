#!/usr/bin/env python3
"""
Benchmark script for FastAPI microservice.
Runs predefined test cases against a running server and measures performance.
"""
import asyncio
import json
import time
import argparse
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

import httpx
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text

from benchmark.test_cases import get_all_test_cases, get_test_cases_by_category


@dataclass
class BenchmarkResult:
    """Result of a single benchmark test case."""
    name: str
    endpoint: str
    method: str
    status_code: int
    expected_status: int
    response_time: float
    success: bool
    error_message: Optional[str] = None
    response_size: Optional[int] = None


@dataclass
class BenchmarkSummary:
    """Summary of all benchmark results."""
    total_tests: int
    successful_tests: int
    failed_tests: int
    average_response_time: float
    min_response_time: float
    max_response_time: float
    total_time: float


class BenchmarkRunner:
    """Main benchmark runner class."""
    
    def __init__(self, base_url: str, auth_token: str, webhook_auth_token: str):
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.webhook_auth_token = webhook_auth_token
        self.console = Console()
        self.results: List[BenchmarkResult] = []
    
    def load_test_cases(self, config_path: str = None, category: str = None) -> List[Dict[str, Any]]:
        """Load test cases from Python configuration."""
        try:
            if category:
                return get_test_cases_by_category(category)
            else:
                return get_all_test_cases()
        except Exception as e:
            self.console.print(f"[red]Error: Failed to load test cases: {e}[/red]")
            raise
    
    def substitute_variables(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Substitute environment variables in test case."""
        def substitute_recursive(obj):
            if isinstance(obj, dict):
                return {k: substitute_recursive(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [substitute_recursive(item) for item in obj]
            elif isinstance(obj, str):
                return obj.replace('${AUTH_TOKEN}', self.auth_token).replace('${WEBHOOK_AUTH_TOKEN}', self.webhook_auth_token)
            else:
                return obj
        
        return substitute_recursive(test_case)
    
    async def run_single_test(self, test_case: Dict[str, Any]) -> BenchmarkResult:
        """Run a single test case and return the result."""
        # Substitute variables
        test_case = self.substitute_variables(test_case)
        
        name = test_case['name']
        endpoint = test_case['endpoint']
        method = test_case['method'].upper()
        headers = test_case.get('headers', {})
        body = test_case.get('body')
        expected_status = test_case['expected_status']
        
        url = f"{self.base_url}{endpoint}"
        
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                if method == 'GET':
                    response = await client.get(url, headers=headers)
                elif method == 'POST':
                    response = await client.post(url, json=body, headers=headers)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response_time = time.time() - start_time
                
                return BenchmarkResult(
                    name=name,
                    endpoint=endpoint,
                    method=method,
                    status_code=response.status_code,
                    expected_status=expected_status,
                    response_time=response_time,
                    success=response.status_code == expected_status,
                    response_size=len(response.content) if response.content else 0
                )
        
        except Exception as e:
            response_time = time.time() - start_time
            return BenchmarkResult(
                name=name,
                endpoint=endpoint,
                method=method,
                status_code=0,
                expected_status=expected_status,
                response_time=response_time,
                success=False,
                error_message=str(e)
            )
    
    async def run_benchmark(self, test_cases: List[Dict[str, Any]]) -> List[BenchmarkResult]:
        """Run all test cases and return results."""
        self.console.print(f"[bold blue]Running benchmark against: {self.base_url}[/bold blue]")
        self.console.print(f"[blue]Total test cases: {len(test_cases)}[/blue]\n")
        
        results = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Running tests...", total=len(test_cases))
            
            for i, test_case in enumerate(test_cases):
                progress.update(task, description=f"Running: {test_case['name']}")
                
                result = await self.run_single_test(test_case)
                results.append(result)
                
                progress.advance(task)
        
        self.results = results
        return results
    
    def print_results(self):
        """Print benchmark results in a formatted table."""
        if not self.results:
            self.console.print("[red]No results to display[/red]")
            return
        
        # Create results table
        table = Table(title="Benchmark Results")
        table.add_column("Test Name", style="cyan")
        table.add_column("Endpoint", style="magenta")
        table.add_column("Method", style="yellow")
        table.add_column("Status", style="green")
        table.add_column("Expected", style="blue")
        table.add_column("Response Time (ms)", style="red")
        table.add_column("Success", style="green")
        table.add_column("Error", style="red")
        
        for result in self.results:
            status_color = "green" if result.success else "red"
            success_text = "✓" if result.success else "✗"
            
            table.add_row(
                result.name,
                result.endpoint,
                result.method,
                str(result.status_code),
                str(result.expected_status),
                f"{result.response_time * 1000:.2f}",
                f"[{status_color}]{success_text}[/{status_color}]",
                result.error_message or ""
            )
        
        self.console.print(table)
    
    def print_summary(self):
        """Print benchmark summary statistics."""
        if not self.results:
            return
        
        successful_tests = sum(1 for r in self.results if r.success)
        failed_tests = len(self.results) - successful_tests
        response_times = [r.response_time for r in self.results]
        
        summary = BenchmarkSummary(
            total_tests=len(self.results),
            successful_tests=successful_tests,
            failed_tests=failed_tests,
            average_response_time=sum(response_times) / len(response_times),
            min_response_time=min(response_times),
            max_response_time=max(response_times),
            total_time=sum(response_times)
        )
        
        # Create summary panel
        summary_text = f"""
Total Tests: {summary.total_tests}
Successful: {summary.successful_tests}
Failed: {summary.failed_tests}
Success Rate: {(summary.successful_tests / summary.total_tests) * 100:.1f}%

Average Response Time: {summary.average_response_time * 1000:.2f} ms
Min Response Time: {summary.min_response_time * 1000:.2f} ms
Max Response Time: {summary.max_response_time * 1000:.2f} ms
Total Time: {summary.total_time:.2f} s
        """.strip()
        
        panel = Panel(
            summary_text,
            title="Benchmark Summary",
            border_style="green" if summary.failed_tests == 0 else "yellow"
        )
        
        self.console.print(panel)
    
    def save_results(self, output_path: str):
        """Save benchmark results to JSON file."""
        results_data = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "summary": asdict(self.get_summary()),
            "results": [asdict(result) for result in self.results]
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results_data, f, indent=2, ensure_ascii=False)
            
            self.console.print(f"[green]Results saved to: {output_path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error saving results: {e}[/red]")
    
    def get_summary(self) -> BenchmarkSummary:
        """Get benchmark summary."""
        if not self.results:
            return BenchmarkSummary(0, 0, 0, 0, 0, 0, 0)
        
        successful_tests = sum(1 for r in self.results if r.success)
        failed_tests = len(self.results) - successful_tests
        response_times = [r.response_time for r in self.results]
        
        return BenchmarkSummary(
            total_tests=len(self.results),
            successful_tests=successful_tests,
            failed_tests=failed_tests,
            average_response_time=sum(response_times) / len(response_times),
            min_response_time=min(response_times),
            max_response_time=max(response_times),
            total_time=sum(response_times)
        )


async def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Benchmark FastAPI microservice")
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
        default=os.getenv("AUTH_TOKEN", "test-auth-token"),
        help="Authentication token (default: from AUTH_TOKEN env var)"
    )
    parser.add_argument(
        "--webhook-auth-token",
        default=os.getenv("WEBHOOK_AUTH_TOKEN", "test-webhook-token"),
        help="Webhook authentication token (default: from WEBHOOK_AUTH_TOKEN env var)"
    )
    
    args = parser.parse_args()
    
    # Create benchmark runner
    runner = BenchmarkRunner(args.url, args.auth_token, args.webhook_auth_token)
    
    try:
        # Load test cases
        test_cases = runner.load_test_cases(category=args.category)
        
        # Run benchmark
        await runner.run_benchmark(test_cases)
        
        # Print results
        runner.print_results()
        runner.print_summary()
        
        # Save results if output path specified
        if args.output:
            runner.save_results(args.output)
        else:
            # Save to default location
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_output = f"benchmark/results/benchmark_{timestamp}.json"
            os.makedirs("benchmark/results", exist_ok=True)
            runner.save_results(default_output)
    
    except KeyboardInterrupt:
        print("\nBenchmark interrupted by user")
    except Exception as e:
        print(f"Benchmark failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
