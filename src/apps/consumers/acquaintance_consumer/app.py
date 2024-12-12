from config.settings import settings
from src.apps.consumers.acquaintance_consumer.acquaintance_consumer import AcquaintanceRabbit
from src.apps.consumers.base.runner import ConsumerRunner


if __name__ == '__main__':
    runner = ConsumerRunner(AcquaintanceRabbit(), settings.ACQUAINTANCE_QUEUE_NAME)
    runner.run()