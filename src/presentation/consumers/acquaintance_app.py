"""Entry point for the acquaintance consumer service."""

from config.settings import settings
from src.infrastructure.rabbit.consumer_runner import ConsumerRunner
from src.main.container import create_acquaintance_consumer
from src.presentation.consumers.consumer_app import ConsumerApp

consumer = create_acquaintance_consumer()
runner = ConsumerRunner(consumer, settings.ACQUAINTANCE_QUEUE_NAME)
app = ConsumerApp(runner, settings.ACQUINTANCE_CONSUMER_PORT)

if __name__ == '__main__':
    app.build()

