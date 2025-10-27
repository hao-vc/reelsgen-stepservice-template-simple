# Testing and Benchmarking

This directory contains testing and benchmarking tools for the FastAPI microservice.

## Testing

### Running Tests

```bash
# Install test dependencies
uv sync --extra dev

# Run all tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run tests with verbose output
pytest -v
```

### Test Structure

- `tests/conftest.py` - Pytest configuration and fixtures
- `tests/test_api.py` - Integration tests for API endpoints
- `tests/unit/test_services.py` - Unit tests for services

### Test Coverage

The test suite covers:
- Health check endpoint
- Operations endpoint
- Step call endpoint
- Example endpoint
- Authentication
- Error handling
- Service layer functionality

## Benchmarking

### Running Benchmarks

```bash
# Run benchmark against local server
python benchmark/benchmark.py --url http://localhost:8000

# Run benchmark against remote server
python benchmark/benchmark.py --url https://your-server.com

# Run specific category of tests
python benchmark/benchmark.py --category health
python benchmark/benchmark.py --category operations
python benchmark/benchmark.py --category example
python benchmark/benchmark.py --category errors

# Save results to specific file
python benchmark/benchmark.py --output results.json

# Use custom auth tokens
python benchmark/benchmark.py --auth-token your-token --webhook-auth-token your-webhook-token
```

### Benchmark Configuration

The benchmark uses `benchmark/test_cases.py` which contains predefined test cases organized by categories:

- **health** - Health check tests
- **operations** - Operations processing tests  
- **step** - Step call tests
- **example** - Example endpoint tests
- **errors** - Error handling tests
- **performance** - Performance tests with large data
- **edge** - Edge cases and boundary conditions

### Benchmark Results

Results are saved in JSON format with:
- Test case details
- Response times
- Success/failure status
- Error messages
- Summary statistics

### Customizing Test Cases

You can customize test cases by modifying `benchmark/test_cases.py`:

```python
def get_custom_test_cases() -> List[Dict[str, Any]]:
    """Get custom test cases for specific scenarios."""
    return [
        {
            "name": "Custom Test",
            "endpoint": "/your-endpoint",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer ${AUTH_TOKEN}"
            },
            "body": {
                "your_data": "value"
            },
            "expected_status": 200,
            "description": "Description of your test"
        }
    ]
```

### Available Categories

- `health` - Health check endpoint tests
- `operations` - General operations processing tests
- `step` - Step call endpoint tests
- `example` - Example text processing tests
- `errors` - Error handling and validation tests
- `performance` - Performance tests with large data
- `edge` - Edge cases and boundary conditions

### Environment Variables

Set these environment variables for testing:

```bash
export AUTH_TOKEN="your-auth-token"
export WEBHOOK_AUTH_TOKEN="your-webhook-token"
```

Or use the `--auth-token` and `--webhook-auth-token` command line arguments.
