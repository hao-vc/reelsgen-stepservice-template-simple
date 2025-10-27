#!/usr/bin/env python3
"""
Simple test runner script for the FastAPI microservice.
"""
import subprocess
import sys
import os
from pathlib import Path


def run_command(command: list, description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print('='*50)
    
    try:
        result = subprocess.run(command, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {command[0]}")
        return False


def main():
    """Main function to run tests."""
    print("FastAPI Microservice Test Runner")
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
    
    success_count = 0
    total_tests = 0
    
    # Install dependencies
    total_tests += 1
    if run_command(["uv", "sync", "--extra", "dev"], "Installing dependencies"):
        success_count += 1
    
    # Run linting
    total_tests += 1
    if run_command(["uv", "run", "black", "--check", "app/", "tests/", "benchmark/"], "Code formatting check"):
        success_count += 1
    
    # Run type checking
    total_tests += 1
    if run_command(["uv", "run", "mypy", "app/"], "Type checking"):
        success_count += 1
    
    # Run tests
    total_tests += 1
    if run_command(["uv", "run", "pytest", "-v"], "Running tests"):
        success_count += 1
    
    # Run tests with coverage
    total_tests += 1
    if run_command(["uv", "run", "pytest", "--cov=app", "--cov-report=term-missing"], "Running tests with coverage"):
        success_count += 1
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Test Summary: {success_count}/{total_tests} passed")
    print('='*50)
    
    if success_count == total_tests:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
