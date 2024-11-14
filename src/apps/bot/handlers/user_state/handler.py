import logging

from aiogram.types import Message

from src.apps.consumers.user_state_consumer.schema.update_user_state import UpdateUserData
from .router import router
from aiogram import F

from src.apps.bot.messages.update_state import ACTIVATION_REQUEST_SENT, PROFILE_HAS_BEEN_ACTIVATED, PROFILE_HAS_NOT_BEEN_ACTIVATED

from config.settings import settings

from ...producers.user_state_producer import UserStateProducer

logger = logging.getLogger(__name__)

user_state_producer = UserStateProducer()

@router.message(F.text == '/activate')
async def activate_profile(message: Message):

    logger.info("Start activating profile...")

    await message.answer(ACTIVATION_REQUEST_SENT)

    user_id = message.from_user.id

    update_user_data = UpdateUserData(user_id=user_id, is_active=True)

    async with user_state_producer as producer:
        logger.info("Producing message...")
        await producer.base_produce_message(update_user_data, settings.UPDATE_USER_QUEUE_NAME)
        await producer.wait_answer_for_user(
            settings.UPDATE_USER_QUEUE_NAME,
            user_id,
            lambda is_success: __push_set_active_answer(is_success, message),
        )

async def __push_set_active_answer(is_success: bool, message: Message):
    answer = PROFILE_HAS_BEEN_ACTIVATED if is_success else PROFILE_HAS_NOT_BEEN_ACTIVATED
    await message.answer(answer)

@router.message(F.text == '/deactivate')
async def deactivate_profile(message: Message):
    pass
