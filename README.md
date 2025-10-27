# Шаблон для быстрого старта собственного StepService для проекта reelsgen

## Возможности

- ✅ **Endpoint проверки состояния (Health Check)** — мониторинг статуса сервиса
- ✅ **Структурированное логирование** — JSON-логи с метками сервиса и endpoint'а
- ✅ **Аутентификация через Bearer Token** — простая токен-авторизация
- ✅ **Webhook-система** — асинхронная отправка результатов по указанному URL
- ✅ **Система алертов** — уведомления об ошибках через Supabase Edge Functions
- ✅ **Step-схемы** — гибкая интеграция с внешними сервисами
- ✅ **Пример эндпоинта** — демонстрация обработки текста
- ✅ **Stateless-архитектура** — отсутствие постоянного состояния между запросами
- ✅ **Деплой на Vercel** — готово к serverless-развертыванию

## Быстрый старт

### 1. Установка зависимостей

```bash
# Рекомендуется установка через uv
uv sync
```

### 2. Настройка окружения

Создайте файл `.env` на основе `.env.example`:

```env
# Конфигурация сервиса
SERVICE_NAME=my-service
SERVICE_VERSION=1.0.0
DEBUG=false

# Аутентификация
AUTH_TOKEN=your-secure-token-here # токен для авторизации входящих запросов
WEBHOOK_AUTH_TOKEN=your-webhook-auth-token-here # токен для авторизации при отправке webhook

# Система алертов (опционально) # можно настроить алерты через https://tg-alerting-systems.lovable.app/
ALERT_WEBHOOK_URL=https://your-project.supabase.co/functions/v1/send-notification
ALERT_API_KEY=your-supabase-api-key

# Логирование
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### 3. Запуск сервиса

```bash
# Запуск в режиме разработки
python main.py
```

## License

MIT License - feel free to use this template for your projects!
