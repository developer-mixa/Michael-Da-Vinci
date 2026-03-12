"""Entry point for the user state consumer service."""

from config.settings import settings
from src.infrastructure.rabbit.consumer_runner import ConsumerRunner
from src.main.container import create_user_state_consumer
from src.presentation.consumers.consumer_app import ConsumerApp

consumer = create_user_state_consumer()
runner = ConsumerRunner(consumer, settings.UPDATE_USER_QUEUE_NAME)
app = ConsumerApp(runner, settings.USER_STATE_CONSUMER_PORT)

if __name__ == '__main__':
    app.build()

