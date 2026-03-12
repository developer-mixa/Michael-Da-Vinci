# Michael-Da-Vinci - Telegram Bot for Dating

## Описание

Telegram бот для организации онлайн-знакомств. Бот предоставляет функционал для поиска партнёров, регистрации, управления профилем и взаимных лайков.

## Архитектура

Проект организован по принципам **Clean Architecture** (Чистая архитектура):

```
src/
├── domain/            # Бизнес-логика и правила (не зависит ни от чего)
│   ├── entities/      # Сущности: User, Like
│   ├── exceptions.py  # Доменные исключения
│   ├── interfaces/    # Абстрактные интерфейсы (порты)
│   └── validators/    # Валидация имени, даты рождения
│
├── application/       # Use Cases — оркестрация бизнес-логики
│   ├── dto/           # Data Transfer Objects (вход/выход use cases)
│   └── use_cases/     # RegisterUser, SearchAcquaintance, LikeUser, UpdateUserState
│
├── infrastructure/    # Реализации внешних зависимостей (адаптеры)
│   ├── database/      # SQLAlchemy модели, репозитории, маппёры
│   ├── rabbit/        # RabbitMQ: BaseConsumer, ConsumerRunner
│   ├── redis/         # Redis: RedisCache (реализация ICache)
│   ├── storage/       # MinIO S3: S3FileStorage (реализация IFileStorage)
│   └── metrics/       # Prometheus метрики (бот + консьюмеры)
│
├── presentation/      # Точки входа (UI / интерфейсы)
│   ├── bot/           # Aiogram: хэндлеры, клавиатуры, сообщения, middleware
│   ├── api/           # FastAPI: /analytics/metrics (Prometheus)
│   └── consumers/     # RabbitMQ консьюмеры (registration, acquaintance, user_state)
│
├── main/              # Точка входа приложения
│   ├── app.py         # FastAPI app + bot runner
│   └── container.py   # Composition Root (DI-контейнер)
│
└── core/              # Общие утилиты (время, аналитика)
```

### Принцип зависимостей

```
Domain ← Application ← Infrastructure
                     ← Presentation
```

- **Domain** — ни от чего не зависит (чистый Python)
- **Application** — зависит только от Domain (интерфейсы)
- **Infrastructure** — реализует интерфейсы Domain
- **Presentation** — вызывает Use Cases через DI-контейнер

## Технологии

- Python 3.10+
- Aiogram 3 (Telegram Bot API)
- FastAPI (HTTP API, webhook)
- SQLAlchemy 2 (async, PostgreSQL)
- RabbitMQ + aio-pika (очереди сообщений)
- Redis (FSM storage, кэширование)
- MinIO (S3-совместимое файловое хранилище)
- Prometheus (метрики)
- Docker & Docker Compose

## Установка

1. Убедитесь, что у вас установлен Docker и Docker Compose.

2. Клонируйте репозиторий:

```bash
git clone https://github.com/developer-mixa/Michael-Da-Vinci.git
cd Michael-Da-Vinci
```

3. Создайте файл `.env` (см. раздел «Настройка»).

4. Запустите все контейнеры:

```bash
docker-compose up --build
```

5. Бот будет доступен через Telegram. Отправьте ему `/start`.

## Настройка

Файл `.env` в корне проекта:

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
REDIS_PASSWORD=your_redis_password

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

```bash
source .venv/bin/activate
pytest
```

### Запуск с покрытием

```bash
pytest --cov=src/domain --cov=src/application --cov=src/infrastructure/rabbit --cov-report=term-missing
```

Текущее покрытие: ~75% по domain + application + infrastructure/rabbit.

## Функции

- Регистрация пользователей с валидацией данных
- Поиск партнёров с ранжированием (по возрасту и лайкам)
- Система взаимных лайков с уведомлениями
- Активация / деактивация профиля
- Редактирование профиля (имя, описание)
- Аналитика: RPS, время выполнения, количество сообщений (Prometheus)
- Swagger UI: `/swagger`
- Метрики Prometheus: `/analytics/metrics`
- Webhook / Polling режим бота

## Как это работает

1. Бот получает входящие сообщения от пользователей через Telegram Bot API (aiogram).
2. Сообщения отправляются в очередь RabbitMQ для обработки.
3. Консьюмеры обрабатывают сообщения, вызывая Use Cases, которые работают с репозиториями.
4. Результат публикуется обратно в очередь, и бот отвечает пользователю.
