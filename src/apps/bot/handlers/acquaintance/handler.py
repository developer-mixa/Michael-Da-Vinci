import base64
import logging
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F
from config.settings import settings
from src.apps.bot.bot import get_bot
from src.apps.bot.emoji.emojies import STOP, LIKE, DISLIKE
from src.apps.bot.handlers.states.acquaintance import Acquaintance
from src.apps.bot.keyboards.acquaintance import CHOISES
from src.apps.bot.producers.acquaintance_producer import AcquaintanceProducer
from src.apps.consumers.acquaintance_consumer.schema.acquintance_data import MutualityData, SearchAcquaintanceData, LikeUserData
from src.apps.consumers.acquaintance_consumer.schema.responses.__main__ import AcquaintanceResponse, AcquaintanceResponseStatus, LikedResponseStatus
from src.apps.consumers.common.user_data import UserData
from src.apps.consumers.register_consumer.schema.registration import RegistrationData
from .router import router
from src.apps.bot.commands.commands import FIND_LOVE
from aiogram.types import ReplyKeyboardRemove
from src.apps.bot.messages import acquaintance as msg
from aiogram.types.input_file import InputFile, BufferedInputFile


acquaintance_producer = AcquaintanceProducer()

logger = logging.getLogger(__name__)

@router.message(F.text == FIND_LOVE)
async def start_find(message: Message, state: FSMContext):
    # finding love...

    await state.clear()
    await state.set_state(Acquaintance.finding)
    await send_acquaintance_answer(message, state)

# Через state сделать

@router.message(Acquaintance.finding)
async def finding(message: Message, state: FSMContext):

    message_text = message.text

    if message_text == STOP:
        await state.clear()
        await message.answer(msg.STOP_SEARCHING, reply_markup=ReplyKeyboardRemove())
    elif message_text == LIKE:
        liked_user_data = await state.get_data()
        liked_user_id = liked_user_data['current_user_id']
        liked_data = LikeUserData(user_id=message.from_user.id, liked_user_id=liked_user_id, action='like_user')
        async with acquaintance_producer as producer:
            await producer.base_produce_message(liked_data, settings.ACQUAINTANCE_QUEUE_NAME)
            await producer.wait_answer_for_user(
                settings.ACQUAINTANCE_LIKE_QUEUE_NAME,
                message.from_user.id,
                lambda response: __push_liked_answer(response, message)
            )
        await send_acquaintance_answer(message, state)
    elif message_text == DISLIKE:
        await send_acquaintance_answer(message, state)
    else:
        await message.answer(msg.ACQUAINTANCE_REQUIREMENTS)

async def send_acquaintance_answer(message: Message, state: FSMContext):
    user_id = message.from_user.id
    search_data = SearchAcquaintanceData(user_id=user_id, action='search')
    async with acquaintance_producer as producer:
        await producer.base_produce_message(search_data, settings.ACQUAINTANCE_QUEUE_NAME)
        await producer.wait_answer_for_user(
            settings.ACQUAINTANCE_QUEUE_NAME,
            user_id,
            lambda response: __push_search_answer(response, message, state)
        )

async def __push_search_answer(response: AcquaintanceResponse, message: Message, state: FSMContext):
    search_response = AcquaintanceResponseStatus.deserialize(response['response'])
    if search_response == AcquaintanceResponseStatus.FOUND:
        found_user_data: UserData = response['data']
        image_input_file = BufferedInputFile(found_user_data['image'], found_user_data['name'])
        await message.answer_photo(photo=image_input_file, caption=f'''
        {found_user_data["name"]}, {found_user_data["age"]}
        
        {found_user_data['description']}
        ''', reply_markup=CHOISES)
        await state.set_data({'current_user_id': found_user_data['user_id']})
    elif search_response == AcquaintanceResponseStatus.NON_REGISTERED:
        await message.answer('Вы не зарегестрированы!')
    elif search_response == AcquaintanceResponseStatus.NOT_FOUND:
        await message.answer('К сожалению, не найдено ни одного пользователя =(')
    elif search_response == AcquaintanceResponseStatus.UNEXCEPTED_ERROR:
        await message.answer('Что-то пошло не так... Попробуйте ещё раз или обратитесь к разработчику')

async def __push_liked_answer(response: AcquaintanceResponse, message: Message):
    liked_response = LikedResponseStatus.deserialize(response['response'])
    if liked_response == LikedResponseStatus.MUTUALLY:
        bot = get_bot()
        mutually_data: MutualityData = response['data']
        liked_user_chat = await bot.get_chat(mutually_data['liked_user_id'])
        liked_username = liked_user_chat.username
        liked_text = 'Вы взаимно лайкнули друг друга, теперь вы можете продолжить в чате: @{username}'
        await message.answer(liked_text.format(username=liked_username))
        await bot.send_message(mutually_data['liked_user_id'], liked_text.format(username=message.from_user.username))
    elif liked_response == LikedResponseStatus.LIKE_SENT:
        logger.info('Like successfully delivered from %s', message.from_user.id)
    else:
        logger.info('Something went wrong... %s', liked_response)
        await message.answer('Что-то пошло не так... Попробуйте ещё раз или обратитесь к разработчику')