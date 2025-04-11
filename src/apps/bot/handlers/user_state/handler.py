import logging

from aiogram.types import Message, CallbackQuery

from src.apps.bot.handlers.states.update_profile import UpdateProfile
from src.apps.consumers.user_state_consumer.schema.update_user_state import UpdateUserData
from .router import router
from aiogram import F

from src.apps.bot.messages import update_state as msg

from src.apps.bot.commands.commands import ACTIVATING, DEACTIVATING, UPDATE_STATE, CALLBACK_UPDATE, CALLBACK_BACK_MENU

from config.settings import settings

from src.apps.bot.keyboards.update_profile import inline_user_state_fields, BACK_TO_MENU

from ...producers.user_state_producer import UserStateProducer
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove


logger = logging.getLogger(__name__)

user_state_producer = UserStateProducer()

@router.message(F.text == ACTIVATING)
async def activate_profile(message: Message):
    await __set_active_profile(message, True)

@router.message(F.text == DEACTIVATING)
async def deactivate_profile(message: Message):
    await __set_active_profile(message, False)

@router.message(F.text == UPDATE_STATE)
async def update_profile(message: Message):
    await message.answer(msg.WHAT_TO_UPDATE, reply_markup=await inline_user_state_fields())

@router.callback_query(F.data == CALLBACK_UPDATE)
async def update_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.edit_text('Меняйте имя', reply_markup=BACK_TO_MENU)
    await state.set_state(UpdateProfile.update_field)

@router.message(UpdateProfile.update_field)
async def fill_update_info(message: Message, state: FSMContext):
    await state.update_data(update_field=message.text)
    await state.clear()
    await message.answer('Изменения приняты', reply_markup=ReplyKeyboardRemove())

@router.callback_query(F.data == CALLBACK_BACK_MENU)
async def back_to_menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.clear()
    await callback.message.edit_text(msg.WHAT_TO_UPDATE, reply_markup=await inline_user_state_fields())

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
