# FastAPI Microservice Template - Developer Guide

## 🚀 Быстрый старт

### Установка и запуск
```bash
# Установка зависимостей
uv sync

# Настройка окружения
cp .env.example .env
# Отредактируйте .env файл

# Запуск сервиса
python main.py
```

### Основные endpoints
- `GET /health` - проверка состояния сервиса
- `POST /example/process-text` - пример обработки текста
- `POST /operations/process` - общий endpoint для операций
- `GET /docs` - Swagger документация

## 🏗️ Архитектура

### Структура проекта
```
app/
├── main.py              # Точка входа FastAPI
├── config.py            # Конфигурация через Pydantic Settings
├── auth.py              # Middleware аутентификации
├── logging_config.py    # Настройка структурированного логирования
├── api/                 # API endpoints
│   ├── health.py        # Health check
│   ├── example.py       # Пример обработки текста
│   └── operations.py    # Общие операции
├── schemas/             # Pydantic модели
│   ├── step_schemas.py  # Схемы для Step API
│   ├── health.py        # Схемы health check
│   └── operations.py    # Схемы операций
└── services/            # Бизнес-логика
    ├── webhook_service.py    # Отправка webhook'ов
    ├── alert_service.py      # Система алертов
    └── operation_service.py # Обработка операций
```

## 🔧 Ключевые компоненты

### 1. Конфигурация (`app/config.py`)
- Валидация переменных окружения через Pydantic Settings
- Обязательные токены аутентификации
- Настройки логирования и алертов

### 2. Аутентификация (`app/auth.py`)
- Bearer Token middleware
- Публичные endpoints (health, docs)
- Логирование попыток аутентификации

### 3. Логирование (`app/logging_config.py`)
- JSON-формат для структурированных логов
- Метки: service, endpoint, operation_id
- Уровни: DEBUG, INFO, WARNING, ERROR

### 4. Webhook система (`app/services/webhook_service.py`)
- Асинхронная отправка результатов
- Авторизация через WEBHOOK_AUTH_TOKEN
- Обработка ошибок HTTP

### 5. Система алертов (`app/services/alert_service.py`)
- Интеграция с Supabase Edge Functions
- Уведомления об ошибках 400/500
- Структурированные алерты с метаданными

## 📝 Step API схемы

### Входящий запрос (`StepCall`)
```python
{
  "step": {"id": "uuid"},
  "webhook": {"url": "https://..."},
  "initial": {"input": {...}},
  "variables": {...}
}
```

### Ответ (`StepResult`)
```python
{
  "step": {"id": "uuid"},
  "operation": {"operation_id": "uuid"},
  "variables": {...},
  "outputs": [{"data": {...}}]
}
```

## 🧪 Тестирование

### Запуск тестов
```bash
# Все тесты
python run_tests.py

# С покрытием
pytest --cov=app tests/
```

### Структура тестов
- `tests/test_api.py` - интеграционные тесты API
- `tests/unit/test_services.py` - unit тесты сервисов
- `tests/conftest.py` - фикстуры и моки

## 📊 Бенчмаркинг

### Запуск бенчмарков
```bash
python run_benchmark.py
```

### Тест-кейсы
- Health check
- Обработка текста
- Ошибки аутентификации
- Валидация данных

## 🔄 Workflow обработки запроса

1. **Получение запроса** → логирование
2. **Аутентификация** → проверка Bearer token
3. **Валидация** → Pydantic схемы
4. **Немедленный ответ** → 204 + X-Operation-ID
5. **Фоновая обработка** → BackgroundTasks
6. **Отправка результата** → webhook
7. **Логирование** → результат операции

## 🚀 Деплой на Vercel

### Конфигурация (`vercel.json`)
```json
{
  "version": 2,
  "builds": [{"src": "app/main.py", "use": "@vercel/python"}],
  "routes": [{"src": "/(.*)", "dest": "app/main.py"}]
}
```

### Переменные окружения в Vercel
- `SERVICE_NAME`, `SERVICE_VERSION`
- `AUTH_TOKEN`, `WEBHOOK_AUTH_TOKEN`
- `ALERT_WEBHOOK_URL`, `ALERT_API_KEY`
- `LOG_LEVEL`, `LOG_FORMAT`

## 🎯 Философия шаблона

### Максимальная гибкость
- Опциональные параметры в `input`
- Обратная совместимость
- Легкое расширение без breaking changes

### Stateless архитектура
- Никакого состояния между запросами
- Независимая обработка каждого запроса
- Простота для начинающих разработчиков

### Готовность к продакшену
- Структурированное логирование
- Система мониторинга и алертов
- Обработка ошибок
- Валидация конфигурации

## 🔧 Расширение шаблона

### Добавление нового endpoint
1. Создать роутер в `app/api/`
2. Добавить схемы в `app/schemas/`
3. Реализовать сервис в `app/services/`
4. Подключить роутер в `main.py`

### Добавление новых параметров
1. Расширить `input` в схемах
2. Добавить обработку в сервисе
3. Обновить тесты и бенчмарки

## 📚 Полезные ссылки

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Structlog](https://www.structlog.org/)
- [Vercel Python](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
