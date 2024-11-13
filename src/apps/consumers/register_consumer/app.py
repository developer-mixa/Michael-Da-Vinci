from src.apps.consumers.register_consumer.register_updates_rabbit import RegisterUpdatesRabbit
from config.settings import settings
from src.apps.consumers.base.runner import ConsumerRunner

if __name__ == '__main__':
    runner = ConsumerRunner(RegisterUpdatesRabbit(), settings.REGISTRATION_QUEUE_NAME)
    runner.run()