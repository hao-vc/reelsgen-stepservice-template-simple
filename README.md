# Template для быстрого создания своих StepService's для проекта reelsgen

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
```

### 2. Configure Environment

Create a `.env` file based on `.env.example`:

```env
# Service Configuration
SERVICE_NAME=my-service
SERVICE_VERSION=1.0.0
DEBUG=false

# Authentication
AUTH_TOKEN=your-secure-token-here # токен для авторизации в данном сервисе
WEBHOOK_AUTH_TOKEN=your-webhook-auth-token-here # токен для авторизации в ЕЛДЕ

# Alerting System (Optional) # можно настроить алерт систему в https://tg-alerting-systems.lovable.app/
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
```

## License

MIT License - feel free to use this template for your projects!
