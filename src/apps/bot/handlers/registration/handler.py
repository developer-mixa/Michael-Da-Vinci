import logging

from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config.settings import settings
from src.apps.bot.bot import get_bot
from src.apps.bot.commands.commands import REGISTRATION
from src.apps.bot.keyboards.registration import GENDERS, OK
from src.apps.bot.keyboards.texts import BOY, GIRL, OK as MARKUP_OK
from src.apps.bot.messages import register as msg
from src.apps.bot.validators import errors as validation
from src.apps.bot.validators.validators import AgeValidator, NameValidator
from src.apps.consumers.register_consumer.schema.registration import RegistrationData

from ...producers.registration_producer import RegistrationProducer
from ..states.registration import Registration
from .router import router

import base64

logger = logging.getLogger(__name__)

registration_producer = RegistrationProducer()


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(msg.WELCOME_MESSAGE)


@router.message(F.text == REGISTRATION)
async def start_registration(message: Message, state: FSMContext) -> None:
    await state.set_state(Registration.accept_privacy_policy)
    await message.answer(msg.ACCEPT_PRIVACY_POLICE, reply_markup=OK)


@router.message(Registration.accept_privacy_policy)
async def fill_name(message: Message, state: FSMContext) -> None:
    if message.text != MARKUP_OK:
        await message.answer(msg.OK_TO_CONTINUE, reply_markup=OK)
        return
    await state.update_data(accept_privacy_policy=message.text)
    await state.set_state(Registration.name)
    await message.answer(msg.WHAT_YOUR_NAME, reply_markup=ReplyKeyboardRemove())


@router.message(Registration.name)
async def fill_age(message: Message, state: FSMContext) -> None:
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
async def fill_gender(message: Message, state: FSMContext) -> None:
    answer = msg.WHAT_YOUR_GENDER
    reply_markup = None
    try:
        age = AgeValidator().validate(message)
        await state.update_data(age=age)
        await state.set_state(Registration.gender)
        reply_markup = GENDERS
    except validation.WrongAgeFormatError:
        answer = msg.HOW_OLD_YOU
    finally:
        await message.answer(answer, reply_markup=reply_markup)


@router.message(Registration.gender)
async def fill_about_you(message: Message, state: FSMContext) -> None:
    message_text = message.text
    if message_text != BOY and message_text != GIRL:
        await message.answer(msg.WRONG_GENDER)
        return
    await state.update_data(gender=message_text)
    await state.set_state(Registration.description)
    await message.answer(msg.ABOUT_YOU, reply_markup=ReplyKeyboardRemove())


@router.message(Registration.description)
async def fill_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(Registration.image)
    await message.answer(msg.SEND_YOUR_PHOTO, reply_markup=ReplyKeyboardRemove())


@router.message(Registration.image)
async def fill_image(message: Message, state: FSMContext) -> None:
    if message.photo:

        dowloaded_image = (await get_bot().download(file=message.photo[-1].file_id)).read()
        image_base64 = base64.b64encode(dowloaded_image).decode('utf-8')
        await state.update_data(image=image_base64)

        # dowloaded_image = await get_bot().download(file=message.photo[-1].file_id)
        # await state.update_data(image=dowloaded_image.read())
        data = await state.get_data()
        await message.answer(msg.PUSH_REGISTER_QUERY)
        await state.clear()

        user_id = message.from_user.id

        reg_data = RegistrationData(user_id=user_id, **data)

        async with registration_producer as producer:
            await producer.base_produce_message(reg_data, settings.REGISTRATION_QUEUE_NAME)
            await producer.wait_answer_for_user(
                settings.REGISTRATION_QUEUE_NAME,
                user_id,
                lambda is_success_reg: __push_register_answer(is_success_reg, message),
            )
    else:
        await message.answer(msg.MUST_SEND_PHOTO)


async def __push_register_answer(is_success_reg: bool, message: Message) -> None:
    answer = msg.SUCCESS_REGISTER if is_success_reg else msg.ALREADY_REGISTER
    await message.answer(answer)
