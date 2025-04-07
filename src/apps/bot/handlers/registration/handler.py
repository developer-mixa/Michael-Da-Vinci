from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F
from ..states.registration import Registration
from .router import router
from src.apps.bot.keyboards.registration import OK, GENDERS, LOCATION
from aiogram.types import ReplyKeyboardRemove
from src.apps.bot.validators.validators import NameValidator, AgeValidator
from src.apps.bot.validators import errors as validation
from src.apps.bot.messages import register as msg
from src.apps.bot.keyboards.texts import OK as MARKUP_OK, BOY, GIRL
import aio_pika
import msgpack
from aio_pika import ExchangeType
from src.storage.rabbit import channel_pool
from src.apps.consumer.actions import REGISTER_USER
from config.settings import settings

@router.message(F.text == "/registration")
async def start_registration(message: Message, state: FSMContext):
    await state.set_state(Registration.accept_privacy_policy)
    await message.answer(msg.ACCEPT_PRIVACY_POLICE, reply_markup=OK)

@router.message(Registration.accept_privacy_policy)
async def fill_name(message: Message, state: FSMContext):
    if message.text != MARKUP_OK:
        await message.answer(msg.OK_TO_CONTINUE, reply_markup=OK)
        return
    await state.update_data(accept_privacy_policy=message.text)
    await state.set_state(Registration.name)
    await message.answer(msg.WHAT_YOUR_NAME, reply_markup=ReplyKeyboardRemove())

@router.message(Registration.name)
async def fill_age(message: Message, state: FSMContext):
    answer = msg.HOW_OLD_YOU
    try:
        name = NameValidator().validate(message)
        await state.update_data(name=name)
        await state.set_state(Registration.age)
    except validation.NameCanContainLettersError:
        answer = msg.NAME_CAN_CONTAIN_LETTERS
    except validation.TooLongNameError:
        answer = msg.TOO_LONG_NAME
    except validation.TooShortNameError:
        answer = msg.TOO_SHORT_NAME
    except validation.NameCannotContainSpacesError:
        answer = msg.NAME_CANT_CONTAIN_SPACES
    except validation.NameBeginCannotBeLowercaseError:
        answer = msg.NAME_BEGIN_CANT_BE_LOWER
    finally:
        await message.answer(answer)

@router.message(Registration.age)
async def fill_gender(message: Message, state: FSMContext):
    answer = msg.WHAT_YOUR_GENDER
    reply_markup=None
    try:
        age = AgeValidator().validate(message)
        await state.update_data(age=age)
        await state.set_state(Registration.gender)
        reply_markup = GENDERS
    except validation.AgeMustBeIntegerError:
        answer = msg.AGE_MUST_BE_INT
    except validation.AgeLessThanZeroError:
        answer = msg.AGE_LESS_ZERO
    except validation.TooBigAgeError:
        answer = msg.TOO_BIG_AGE
    finally:
        await message.answer(answer, reply_markup=reply_markup)

@router.message(Registration.gender)
async def fill_gender(message: Message, state: FSMContext):
    message_text = message.text
    if message_text != BOY and message_text != GIRL:
        await message.answer(msg.WRONG_GENDER)
        return
    await state.update_data(gender=message_text)
    await state.set_state(Registration.description)
    await message.answer(msg.ABOUT_YOU, reply_markup=ReplyKeyboardRemove())

@router.message(Registration.description)
async def fill_gender(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Registration.location)
    await message.answer(msg.WHERE_YOU_FROM, reply_markup=LOCATION)

@router.message(Registration.location)
async def fill_location(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(Registration.image)
    await message.answer(msg.SEND_YOUR_PHOTO, reply_markup=ReplyKeyboardRemove())

@router.message(Registration.image)
async def fill_image(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(image=message.photo[-1].file_id)
        data = await state.get_data()

        await message.answer(msg.REGISTER_IS_OVER)
        await state.clear()
        async with channel_pool.acquire() as channel:  # type: aio_pika.Channel
            exchange = await channel.declare_exchange(REGISTER_USER, ExchangeType.TOPIC, durable=True)
            queue = await channel.declare_queue(
                settings.USER_REGISTRATION_QUEUE_TEMPLATE.format(
                    user_id=message.from_user.id,
            ), durable=True
            )
            await queue.bind(
                exchange,
                settings.USER_REGISTRATION_QUEUE_TEMPLATE.format(
                user_id=message.from_user.id,
            ),
        )
            await exchange.publish(
            aio_pika.Message(
                msgpack.packb(
                    GiftMessage(
                        user_id=message.from_user.id,
                        action='get_gifts',
                        event='gift'
                    ))), 'user_messages')
    else:
        await message.answer(msg.MUST_SEND_PHOTO)
