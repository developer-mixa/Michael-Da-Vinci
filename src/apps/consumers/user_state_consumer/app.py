from config.settings import settings
from src.apps.consumers.base.consumer_app import ConsumerApp
from src.apps.consumers.base.runner import ConsumerRunner
from src.apps.consumers.user_state_consumer.update_state_rabbit import UpdateStateRabbit

runner = ConsumerRunner(UpdateStateRabbit(), settings.UPDATE_USER_QUEUE_NAME)
app = ConsumerApp(runner, settings.USER_STATE_CONSUMER_PORT)

if __name__ == '__main__':
    app.build()
