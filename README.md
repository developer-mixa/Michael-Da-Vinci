# Michael-Da-Vinci - Telegram Bot for Dating

## Описание

Этот репозиторий содержит исходный код для Telegram бота, предназначенного для организации онлайн-знакомств. Бот предоставляет функционал для поиска партнеров.

## Технологии

- Python 3.8+
- Telethon (для работы с Telegram Bot API)
- RabbitMQ (для обработки сообщений)
- PostgreSQL (для хранения данных)
- Поддерживается WebHook при указании BOT_WEBHOOK_URL

## Установка

Для установки проекта выполните следующие шаги:

1. Убедитесь, что у вас установлен Docker и Docker Compose.

2. Клонируйте этот репозиторий:
git clone https://github.com/developer-mixa/Michael-Da-Vinci.git cd Michael-Da-Vinci


3. Выполните команду для запуска всех необходимых контейнеров:
docker-compose up --build


4. После успешного запуска, бот будет доступен через Telegram. Отправьте ему команду `/start`, чтобы начать использовать его функционал.

## Настройка

Перед запуском убедитесь, что у вас есть файл `.env` в корневой директории проекта. Он должен содержать следующие переменные окружения:

BOT_TOKEN=your_token
BOT_WEBHOOK_URL=

PG_DBNAME=db_name
PG_USER=db_user
PG_PASSWORD=db_password
PG_HOST=postgres
PG_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379

SERVER_PORT=8000
USER_STATE_CONSUMER_PORT=8001
REGISTRATION_CONSUMER_PORT=8002
ACQUINTANCE_CONSUMER_PORT=8003

MINIO_USER=user
MINIO_PASSWORD=user_password
MINIO_HOST=minio-app


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
