import logging

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types.input_file import BufferedInputFile

from config.settings import settings
from src.apps.bot.bot import get_bot
from src.apps.bot.commands.commands import FIND_LOVE
from src.apps.bot.emoji.emojies import DISLIKE, LIKE, STOP
from src.apps.bot.handlers.states.acquaintance import Acquaintance
from src.apps.bot.keyboards.acquaintance import CHOISES
from src.apps.bot.messages import acquaintance as msg
from src.apps.bot.producers.acquaintance_producer import AcquaintanceProducer
from src.apps.consumers.acquaintance_consumer.actions import LIKE as LIKE_ACTION, SEARCH as SEARCH_ACTION
from src.apps.consumers.acquaintance_consumer.schema.acquintance_data import (
    LikeUserData,
    MutualityData,
    SearchAcquaintanceData,
)
from src.apps.consumers.acquaintance_consumer.schema.responses.responses import (
    AcquaintanceResponse,
    AcquaintanceResponseStatus,
    LikedResponseStatus,
)

from .router import router

acquaintance_producer = AcquaintanceProducer()

logger = logging.getLogger(__name__)


@router.message(F.text == FIND_LOVE)
async def start_find(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(Acquaintance.finding)
    await send_acquaintance_answer(message, state)


@router.message(Acquaintance.finding)
async def finding(message: Message, state: FSMContext) -> None:

    message_text = message.text

    if message_text == STOP:
        await state.clear()
        await message.answer(msg.STOP_SEARCHING, reply_markup=ReplyKeyboardRemove())
    elif message_text == LIKE:
        liked_user_data = await state.get_data()
        liked_user_id = liked_user_data['current_user_id']
        liked_data = LikeUserData(
            user_id=message.from_user.id,
            liked_user_id=liked_user_id,
            action=LIKE_ACTION,
        )
        async with acquaintance_producer as producer:
            await producer.base_produce_message(liked_data, settings.ACQUAINTANCE_QUEUE_NAME)
            await producer.wait_answer_for_user(
                settings.ACQUAINTANCE_LIKE_QUEUE_NAME,
                message.from_user.id,
                lambda response: __push_liked_answer(response, message, state),
            )
    elif message_text == DISLIKE:
        await send_acquaintance_answer(message, state)
    else:
        await message.answer(msg.ACQUAINTANCE_REQUIREMENTS)


async def send_acquaintance_answer(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    search_data = SearchAcquaintanceData(user_id=user_id, action=SEARCH_ACTION)
    async with acquaintance_producer as producer:
        await producer.base_produce_message(search_data, settings.ACQUAINTANCE_QUEUE_NAME)
        await producer.wait_answer_for_user(
            settings.ACQUAINTANCE_QUEUE_NAME, user_id, lambda response: __push_search_answer(response, message, state)
        )


async def __push_search_answer(response: AcquaintanceResponse, message: Message, state: FSMContext) -> None:
    search_response = AcquaintanceResponseStatus.deserialize(response['response'])
    if search_response == AcquaintanceResponseStatus.FOUND:
        found_user_data = response['data']
        image_input_file = BufferedInputFile(found_user_data['image'], found_user_data['name'])
        await message.answer_photo(
            photo=image_input_file,
            caption=msg.USER_INFO_TEMPLATE.format(
                name=found_user_data['name'], age=found_user_data['age'], description=found_user_data['description']
            ),
            reply_markup=CHOISES,
        )
        await state.set_data({'current_user_id': found_user_data['user_id']})
    elif search_response == AcquaintanceResponseStatus.NON_REGISTERED:
        await message.answer(msg.NOT_REGISTERED)
    elif search_response == AcquaintanceResponseStatus.PROFILE_MUST_BE_ACTIVATED:
        await message.answer(msg.PROFILE_MUST_BE_ACTIVATED)
    elif search_response == AcquaintanceResponseStatus.NOT_FOUND:
        await message.answer(msg.NO_USERS_FOUND)
    elif search_response == AcquaintanceResponseStatus.UNEXCEPTED_ERROR:
        await message.answer(msg.SOMETHING_WENT_WRONG)


async def __push_liked_answer(response: AcquaintanceResponse, message: Message, state: FSMContext) -> None:
    liked_response = LikedResponseStatus.deserialize(response['response'])
    if liked_response == LikedResponseStatus.MUTUALLY:
        bot = get_bot()
        mutually_data: MutualityData = response['data']
        liked_user_chat = await bot.get_chat(mutually_data['liked_user_id'])
        liked_username = liked_user_chat.username
        await message.answer(
            msg.MUTUALL_LIKE_TEMPLATE.format(username=liked_username), reply_markup=ReplyKeyboardRemove()
        )
        await bot.send_message(
            mutually_data['liked_user_id'], msg.MUTUALL_LIKE_TEMPLATE.format(username=message.from_user.username)
        )
        await state.clear()
    elif liked_response == LikedResponseStatus.LIKE_SENT:
        logger.info('Like successfully delivered from %s', message.from_user.id)
        await send_acquaintance_answer(message, state)
    else:
        logger.info('Something went wrong... %s', liked_response)
        await message.answer(msg.SOMETHING_WENT_WRONG)
