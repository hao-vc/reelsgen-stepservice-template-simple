# FastAPI Microservice Template

A simple FastAPI microservice template designed for beginners to learn web development and API creation. This template focuses on the fundamentals of FastAPI without complex components like task queues, external databases, or containerization.

## Features

- ✅ **Health Check Endpoint** - Service status monitoring
- ✅ **Structured Logging** - JSON logs with service and endpoint labels
- ✅ **Bearer Token Authentication** - Simple token-based auth
- ✅ **Webhook System** - Asynchronous result delivery
- ✅ **Alert System** - Error notifications via Supabase Edge Functions
- ✅ **Step Schemas** - Flexible external service integration
- ✅ **Example Endpoint** - Text processing demonstration
- ✅ **Stateless Architecture** - No persistent state between requests
- ✅ **Vercel Deployment** - Serverless deployment ready

## Quick Start

### 1. Install Dependencies

```bash
# Install using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### 2. Configure Environment

Create a `.env` file based on `.env.example`:

```env
# Service Configuration
SERVICE_NAME=my-service
SERVICE_VERSION=1.0.0
DEBUG=false

# Authentication
AUTH_TOKEN=your-secure-token-here
WEBHOOK_AUTH_TOKEN=your-webhook-auth-token-here

# Alerting System (Optional)
ALERT_WEBHOOK_URL=https://your-project.supabase.co/functions/v1/send-notification
ALERT_API_KEY=your-supabase-api-key

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### 3. Run the Service

```bash
# Development mode
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Test the Service

```bash
# Health check (no auth required)
curl http://localhost:8000/health

# Process text (auth required)
curl -X POST http://localhost:8000/example/process-text \
  -H "Authorization: Bearer your-secure-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "step": {"id": "550e8400-e29b-41d4-a716-446655440000"},
    "webhook": {"url": "https://webhook.site/your-webhook-url"},
    "initial": {
      "input": {
        "text": "Hello World",
        "operation": "uppercase",
        "language": "en",
        "format": "plain"
      }
    }
  }'
```

## API Endpoints

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service_name": "my-service",
  "version": "1.0.0",
  "uptime": "2h 30m 15s",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Text Processing Example

```http
POST /example/process-text
Authorization: Bearer <token>
Content-Type: application/json

{
  "step": {"id": "550e8400-e29b-41d4-a716-446655440000"},
  "webhook": {"url": "https://client.com/webhook"},
  "initial": {
    "input": {
      "text": "Hello World",
      "operation": "uppercase",
      "language": "en",
      "format": "plain",
      "max_length": 1000,
      "preserve_spaces": true,
      "remove_punctuation": false,
      "add_timestamp": true
    }
  },
  "variables": {
    "timeout": 30,
    "retry_count": 3
  }
}
```

**Response:**
```http
HTTP/1.1 202 Accepted
X-Operation-ID: 550e8400-e29b-41d4-a716-446655440000
```

### General Operations

```http
POST /operations/process
Authorization: Bearer <token>
Content-Type: application/json

{
  "webhook_url": "https://client.com/webhook",
  "data": {
    "input": "some data"
  }
}
```

## Webhook Authentication

The service uses separate authentication tokens for different purposes:

- **`AUTH_TOKEN`** - Used for authenticating incoming requests to the API endpoints
- **`WEBHOOK_AUTH_TOKEN`** - Used for authenticating outgoing webhook requests

When the service sends webhook results, it includes the `WEBHOOK_AUTH_TOKEN` in the `Authorization` header:

```http
Authorization: Bearer <WEBHOOK_AUTH_TOKEN>
```

This allows you to:
- Use different security levels for incoming vs outgoing requests
- Rotate webhook tokens independently from API tokens
- Implement different authentication strategies for webhooks

## Webhook Payloads

The service sends results to your webhook URL with the following formats:

### Step Result (Intermediate)
```json
{
  "step": {"id": "550e8400-e29b-41d4-a716-446655440000"},
  "operation": {"operation_id": "550e8400-e29b-41d4-a716-446655440000"},
  "variables": {"quality": "1080p"},
  "outputs": [
    {
      "data": {
        "processed_text": "HELLO WORLD",
        "operation": "uppercase",
        "length": 11
      }
    }
  ]
}
```

### Final Step Result
```json
{
  "step": {"id": "550e8400-e29b-41d4-a716-446655440000"},
  "operation": {"operation_id": "550e8400-e29b-41d4-a716-446655440000"},
  "videos": [
    {
      "url": "https://example.com/video.mp4",
      "thumbnail": {"url": "https://example.com/thumb.jpg"},
      "channel": {"id": "550e8400-e29b-41d4-a716-446655440001"},
      "description": "Processed video"
    }
  ]
}
```

## Text Processing Operations

The example endpoint supports various text operations with maximum flexibility:

- `uppercase` - Convert to uppercase
- `lowercase` - Convert to lowercase
- `reverse` - Reverse the text
- `title` - Title case
- `capitalize` - Capitalize first letter
- `strip` - Remove leading/trailing whitespace
- `word_count` - Count words
- `char_count` - Count characters

### Optional Parameters

All parameters except `text` are optional for maximum flexibility:

- `operation` - Text processing operation (default: "uppercase")
- `language` - Language code (default: "en")
- `format` - Output format (default: "plain")
- `encoding` - Text encoding (default: "utf-8")
- `max_length` - Maximum output length (default: 1000)
- `preserve_spaces` - Preserve whitespace (default: true)
- `remove_punctuation` - Remove punctuation (default: false)
- `add_timestamp` - Add timestamp prefix (default: true)
- `custom_delimiter` - Custom word delimiter (default: " ")
- `metadata` - Arbitrary metadata object

## Logging

The service uses structured JSON logging with the following format:

```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "level": "INFO",
  "service": "my-service",
  "endpoint": "/example/process-text",
  "operation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Operation started",
  "extra": {
    "user_id": "user123",
    "request_id": "req-456"
  }
}
```

### Log Levels

- `DEBUG` - Detailed information for debugging
- `INFO` - General information about operations
- `WARNING` - Warning messages
- `ERROR` - Error messages
- `CRITICAL` - Critical errors

## Alert System

The service automatically sends alerts for:

- HTTP 400/500 errors
- Unhandled exceptions
- Validation errors

Alerts are sent to a Supabase Edge Function with the following format:

```json
{
  "text": "Error in my-service at /example/process-text: Invalid input",
  "priority": "high",
  "timestamp": "2024-01-15T10:30:00Z",
  "tags": ["error", "incident", "my-service", "operation:550e8400-e29b-41d4-a716-446655440000"],
  "debug_logs": "Error type: ValueError\nEndpoint: /example/process-text\nOperation ID: 550e8400-e29b-41d4-a716-446655440000"
}
```

## Deployment

### Vercel Deployment

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Deploy:**
   ```bash
   vercel
   ```

3. **Set Environment Variables:**
   ```bash
   vercel env add AUTH_TOKEN
   vercel env add WEBHOOK_AUTH_TOKEN
   vercel env add ALERT_WEBHOOK_URL
   vercel env add ALERT_API_KEY
   ```

### Environment Variables

Required:
- `AUTH_TOKEN` - Bearer token for request authentication
- `WEBHOOK_AUTH_TOKEN` - Bearer token for webhook authentication

Optional:
- `SERVICE_NAME` - Service name (default: "my-service")
- `SERVICE_VERSION` - Service version (default: "1.0.0")
- `DEBUG` - Debug mode (default: false)
- `LOG_LEVEL` - Log level (default: INFO)
- `LOG_FORMAT` - Log format (default: json)
- `ALERT_WEBHOOK_URL` - Supabase Edge Function URL
- `ALERT_API_KEY` - Supabase API key

## Testing and Benchmarking

### Running Tests

```bash
# Install test dependencies
uv sync --extra dev

# Run all tests
python run_tests.py

# Or run tests directly
uv run pytest -v

# Run tests with coverage
uv run pytest --cov=app --cov-report=html
```

### Running Benchmarks

```bash
# Run benchmark against local server
python run_benchmark.py --url http://localhost:8000

# Run benchmark against remote server
python run_benchmark.py --url https://your-server.com

# Run specific category of tests
python run_benchmark.py --category health
python run_benchmark.py --category operations
python run_benchmark.py --category example
python run_benchmark.py --category errors

# Save results to specific file
python run_benchmark.py --output results.json
```

### Test Coverage

The test suite covers:
- Health check endpoint
- Operations endpoint
- Step call endpoint
- Example endpoint
- Authentication
- Error handling
- Service layer functionality

### Benchmark Test Cases

The benchmark includes predefined test cases for:
- Health check tests
- Operations processing tests
- Step call tests
- Example endpoint tests
- Error handling tests

See `benchmark/test_cases.py` for configuration details.

## Development

### Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration
│   ├── auth.py                 # Authentication
│   ├── logging_config.py       # Logging setup
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── operations.py
│   │   └── step_schemas.py
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── operations.py
│   │   └── example.py
│   └── services/               # Business logic
│       ├── __init__.py
│       ├── operation_service.py
│       ├── webhook_service.py
│       └── alert_service.py
├── main.py                     # Application entry point
├── pyproject.toml             # Dependencies
├── vercel.json                 # Vercel configuration
└── README.md
```

### Code Quality

```bash
# Format code
black .

# Sort imports
isort .

# Type checking
mypy .

# Run tests (when implemented)
pytest
```

## Philosophy

This template follows the principle of **maximum flexibility**:

- **Optional Parameters**: Maximum number of optional parameters in input schemas
- **Extensibility**: Easy to add new fields without breaking changes
- **Backward Compatibility**: Old clients continue working when new parameters are added
- **Universality**: One microservice can handle various types of tasks

## Learning Objectives

By working with this template, beginners will learn:

- FastAPI fundamentals and async programming
- Structured logging and monitoring
- Authentication and authorization
- Stateless microservice architecture
- Data validation with Pydantic
- Webhook systems and async processing
- Error handling and alerting
- API versioning and documentation
- Deployment on serverless platforms

## License

MIT License - feel free to use this template for your projects!
