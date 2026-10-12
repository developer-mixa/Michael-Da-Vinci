# Michael-Da-Vinci — Telegram-бот знакомств на микросервисах

Бот для онлайн-знакомств: регистрация анкеты, поиск, лайки и взаимные совпадения.
Обработка вынесена в отдельные сервисы-консьюмеры, которые общаются с ботом через RabbitMQ.

## Архитектура

```
Telegram ──webhook / polling──> web (FastAPI + aiogram 3) ──> RabbitMQ ──> register_consumer
                                   │                                  ├──> user_state_consumer
                                   │                                  └──> acquaintance_consumer
                                   └── метрики <── Prometheus                     │
                                                              PostgreSQL · Redis · MinIO
```

- **web** — FastAPI-приложение: принимает Webhook от Telegram (или запускает polling, если webhook не задан),
  обрабатывает апдейты через aiogram 3, отдаёт метрики для Prometheus.
- **register_consumer / user_state_consumer / acquaintance_consumer** — независимые сервисы на aio-pika:
  регистрация анкеты, обновление профиля, подбор пар и лайки.
- **PostgreSQL** — asyncpg + SQLAlchemy 2 (async), миграции через dbmate.
- **Redis** — хранилище FSM-состояний бота (aiogram RedisStorage) и данные для подбора анкет.
- **MinIO (S3)** — хранение файлов.
- **Prometheus** — собственные метрики: RPS бота, время обработки апдейтов, бизнес-аналитика.

## Стек

Python 3.10+, aiogram 3, FastAPI, SQLAlchemy 2 (async), asyncpg, RabbitMQ (aio-pika), Redis, MinIO,
Prometheus, Pydantic v2, Docker Compose, Poetry, pytest.

## Особенности

- Middleware aiogram: подсчёт RPS, замер времени выполнения хендлеров, сбор аналитики, антифлуд.
- Два режима работы: polling для разработки и webhook для продакшена.
- Сквозное логирование (конфиг — `config/logging.conf.yml`).
- Тесты на слой хранения (PostgreSQL, RabbitMQ, Redis) и базовый консьюмер.

## Установка

Для установки проекта выполните следующие шаги:

1. Убедитесь, что у вас установлен Docker и Docker Compose.

2. Клонируйте этот репозиторий:

```bash
git clone https://github.com/developer-mixa/Michael-Da-Vinci.git
cd Michael-Da-Vinci
```

3. Выполните команду для запуска всех необходимых контейнеров:

```bash
docker compose up --build
```

4. После успешного запуска, бот будет доступен через Telegram. Отправьте ему команду `/start`, чтобы начать использовать его функционал.

## Настройка

Перед запуском убедитесь, что у вас есть файл `.env` в корневой директории проекта. Он должен содержать следующие переменные окружения:

```env
BOT_TOKEN=your_token
BOT_WEBHOOK_URL=

PG_DBNAME=db_name
PG_USER=db_user
PG_PASSWORD=db_password
PG_HOST=postgres
PG_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=redis_password

SERVER_PORT=8000
USER_STATE_CONSUMER_PORT=8001
REGISTRATION_CONSUMER_PORT=8002
ACQUINTANCE_CONSUMER_PORT=8003

MINIO_USER=user
MINIO_PASSWORD=user_password
MINIO_HOST=minio-app
```


## Тестирование

### Запуск юнит-тестов

1. Активируйте виртуальное окружение:

```bash
source .venv/bin/activate
```

2. Запустите тесты:

```bash
pytest
```

### Запуск тестов с покрытием

Для оценки покрытия по основным модулям (`src/storage` и `src/apps/consumers/base`) используйте:

```bash
pytest --cov=src/storage --cov=src/apps/consumers/base --cov-report=term-missing
```

Общее покрытие по этим модулям должно быть не ниже 35% (на текущий момент ~55%).

## Функции

- Поиск между пользователями
- Аналитика активности пользователей
- Сквозное логирование
- Интеграция с RabbitMQ для обработки сообщений
- Webhook
1. Бот получает входящие сообщения от пользователей через Telegram Bot API.
2. Эти сообщения отправляются в очередь RabbitMQ для обработки.
3. Консьюмеры в RabbitMQ обрабатывают сообщения и сохраняют информацию в базу данных.
4. Бот отвечает пользователям на основе полученных данных.
