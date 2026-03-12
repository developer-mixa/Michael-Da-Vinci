"""Entry point for the registration consumer service."""

from config.settings import settings
from src.infrastructure.rabbit.consumer_runner import ConsumerRunner
from src.main.container import create_registration_consumer
from src.presentation.consumers.consumer_app import ConsumerApp

consumer = create_registration_consumer()
runner = ConsumerRunner(consumer, settings.REGISTRATION_QUEUE_NAME)
app = ConsumerApp(runner, settings.REGISTRATION_CONSUMER_PORT)

if __name__ == '__main__':
    app.build()

