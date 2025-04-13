from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F
from src.apps.bot.emoji.emojies import STOP, LIKE, DISLIKE
from src.apps.bot.handlers.states.acquaintance import Acquaintance
from src.apps.bot.keyboards.acquaintance import CHOISES
from src.apps.consumers.register_consumer.schema.registration import RegistrationData
from .router import router
from src.apps.bot.commands.commands import FIND_LOVE
from aiogram.types import ReplyKeyboardRemove
from src.apps.bot.messages import acquaintance as msg



@router.message(F.text == FIND_LOVE)
async def start_find(message: Message, state: FSMContext):
    # finding love...

    await state.clear()
    await state.set_state(Acquaintance.finding)
    await send_acquaintance_answer(message)

@router.message(Acquaintance.finding)
async def finding(message: Message, state: FSMContext):

    message_text = message.text

    if message_text == STOP:
        await state.clear()
        await message.answer(msg.STOP_SEARCHING, reply_markup=ReplyKeyboardRemove())
    elif message_text == LIKE:
        # Like action...
        await send_acquaintance_answer(message)
    elif message_text == DISLIKE:
        await send_acquaintance_answer(message)
    else:
        await message.answer(msg.ACQUAINTANCE_REQUIREMENTS)

async def send_acquaintance_answer(message: Message):
    await message.answer(text='Найдена какая-то девушка!!!!!!!!!!!!!!', reply_markup=CHOISES)