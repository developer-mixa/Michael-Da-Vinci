"""Bot handler: Acquaintance / matching flow."""

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types.input_file import BufferedInputFile

from config.settings import settings
from src.application.dto.acquaintance import AcquaintanceStatus, LikeStatus
from src.presentation.bot.bot import get_bot
from src.presentation.bot.commands import FIND_LOVE
from src.presentation.bot.emoji import DISLIKE, LIKE, STOP
from src.presentation.bot.keyboards.acquaintance import CHOISES
from src.presentation.bot.messages import acquaintance as msg
from src.presentation.bot.states.acquaintance import Acquaintance

logger = logging.getLogger(__name__)

router = Router()

# Action constants (for message broker)
SEARCH_ACTION = 'search'
LIKE_ACTION = 'like_user'


def _get_producer():
    from src.main.container import get_acquaintance_producer
    return get_acquaintance_producer()


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
        liked_data = {
            'user_id': message.from_user.id,
            'liked_user_id': liked_user_id,
            'action': LIKE_ACTION,
        }
        producer = _get_producer()
        async with producer as p:
            await p.base_produce_message(liked_data, settings.ACQUAINTANCE_QUEUE_NAME)
            await p.wait_answer_for_user(
                settings.ACQUAINTANCE_LIKE_QUEUE_NAME,
                message.from_user.id,
                lambda response: _push_liked_answer(response, message, state),
            )
    elif message_text == DISLIKE:
        await send_acquaintance_answer(message, state)
    else:
        await message.answer(msg.ACQUAINTANCE_REQUIREMENTS)


async def send_acquaintance_answer(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    search_data = {'user_id': user_id, 'action': SEARCH_ACTION}
    producer = _get_producer()
    async with producer as p:
        await p.base_produce_message(search_data, settings.ACQUAINTANCE_QUEUE_NAME)
        await p.wait_answer_for_user(
            settings.ACQUAINTANCE_QUEUE_NAME, user_id,
            lambda response: _push_search_answer(response, message, state)
        )


async def _push_search_answer(response: dict, message: Message, state: FSMContext) -> None:
    search_response = AcquaintanceStatus(response['response'])
    if search_response == AcquaintanceStatus.FOUND:
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
    elif search_response == AcquaintanceStatus.NON_REGISTERED:
        await message.answer(msg.NOT_REGISTERED)
    elif search_response == AcquaintanceStatus.PROFILE_MUST_BE_ACTIVATED:
        await message.answer(msg.PROFILE_MUST_BE_ACTIVATED)
    elif search_response == AcquaintanceStatus.NOT_FOUND:
        await message.answer(msg.NO_USERS_FOUND)
    elif search_response == AcquaintanceStatus.UNEXPECTED_ERROR:
        await message.answer(msg.SOMETHING_WENT_WRONG)


async def _push_liked_answer(response: dict, message: Message, state: FSMContext) -> None:
    liked_response = LikeStatus(response['response'])
    if liked_response == LikeStatus.MUTUALLY:
        bot = get_bot()
        liked_user_id = response['data']['liked_user_id']
        liked_user_chat = await bot.get_chat(liked_user_id)
        liked_username = liked_user_chat.username
        await message.answer(
            msg.MUTUALL_LIKE_TEMPLATE.format(username=liked_username), reply_markup=ReplyKeyboardRemove()
        )
        await bot.send_message(
            liked_user_id, msg.MUTUALL_LIKE_TEMPLATE.format(username=message.from_user.username)
        )
        await state.clear()
    elif liked_response == LikeStatus.LIKE_SENT:
        logger.info('Like successfully delivered from %s', message.from_user.id)
        await send_acquaintance_answer(message, state)
    else:
        logger.info('Something went wrong... %s', liked_response)
        await message.answer(msg.SOMETHING_WENT_WRONG)

