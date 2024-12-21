from config.settings import settings
from src.apps.consumers.base.consumer_app import ConsumerApp
from src.apps.consumers.base.runner import ConsumerRunner
from src.apps.consumers.register_consumer.register_updates_rabbit import RegisterUpdatesRabbit

runner = ConsumerRunner(RegisterUpdatesRabbit(), settings.REGISTRATION_QUEUE_NAME)
app = ConsumerApp(runner, settings.REGISTRATION_CONSUMER_PORT)

if __name__ == '__main__':
    app.build()
