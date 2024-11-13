from src.apps.consumers.user_state_consumer.update_state_rabbit import UpdateStateRabbit
from config.settings import settings
from src.apps.consumers.base.runner import ConsumerRunner

if __name__ == '__main__':
    runner = ConsumerRunner(UpdateStateRabbit(), settings.UPDATE_USER_QUEUE_NAME)
    runner.run()