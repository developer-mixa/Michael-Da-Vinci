import logging

from aiogram.types import Message

from src.apps.consumers.user_state_consumer.schema.update_user_state import UpdateUserData
from .router import router
from aiogram import F

from src.apps.bot.messages import update_state as msg

from config.settings import settings

from ...producers.user_state_producer import UserStateProducer

logger = logging.getLogger(__name__)

user_state_producer = UserStateProducer()

@router.message(F.text == '/activate')
async def activate_profile(message: Message):
    await __set_active_profile(message, True)

@router.message(F.text == '/deactivate')
async def deactivate_profile(message: Message):
    await __set_active_profile(message, False)

async def __set_active_profile(message: Message, is_active: bool):
    logger.info("Start setting active profile to %s", is_active)

    await message.answer(msg.ACTIVATION_REQUEST_SENT if is_active else msg.DEACTIVATION_REQUEST_SENT)

    user_id = message.from_user.id

    update_user_data = UpdateUserData(user_id=user_id, is_active=is_active)

    async with user_state_producer as producer:
        logger.info("Producing message...")
        await producer.base_produce_message(update_user_data, settings.UPDATE_USER_QUEUE_NAME)
        await producer.wait_answer_for_user(
            settings.UPDATE_USER_QUEUE_NAME,
            user_id,
            lambda is_success: __push_set_active_answer(is_active, is_success, message),
        )
async def __push_set_active_answer(is_active: bool, is_success: bool, message: Message):
    success_msg = msg.PROFILE_HAS_BEEN_ACTIVATED if is_active else msg.PROFILE_HAS_BEEN_DEACTIVATED
    answer = success_msg if is_success else msg.SOMETHING_WENT_WRONG
    await message.answer(answer)
