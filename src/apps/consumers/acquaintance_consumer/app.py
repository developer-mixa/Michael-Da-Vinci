from config.settings import settings
from src.apps.consumers.acquaintance_consumer.acquaintance_consumer import AcquaintanceRabbit
from src.apps.consumers.base.consumer_app import ConsumerApp
from src.apps.consumers.base.runner import ConsumerRunner

runner = ConsumerRunner(AcquaintanceRabbit(), settings.ACQUAINTANCE_QUEUE_NAME)
app = ConsumerApp(runner, settings.ACQUINTANCE_CONSUMER_PORT)

if __name__ == '__main__':
    app.build()
