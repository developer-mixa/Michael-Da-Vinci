from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F
from ..states.registration import Registration
from .router import router
from src.apps.bot.keyboards.registration import OK, GENDERS, LOCATION
from aiogram.types import ReplyKeyboardRemove
from src.apps.bot.validators.validators import NameValidator, AgeValidator, GenderValidator
from src.apps.bot.validators.errors import ValidationError
from src.apps.bot.messages import register as msg
from src.apps.bot.keyboards.texts import OK as MARKUP_OK 

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
    try:
        name = NameValidator().validate(message)
        await state.update_data(name=name)
        await state.set_state(Registration.age)
        await message.answer(msg.HOW_OLD_YOU)
    except ValidationError as e:
        await message.answer(e.message)

@router.message(Registration.age)
async def fill_gender(message: Message, state: FSMContext):
    try:
        age = AgeValidator().validate(message)
        await state.update_data(age=age)
        await state.set_state(Registration.gender)
        await message.answer(msg.WHAT_YOUR_GENDER, reply_markup=GENDERS)
    except ValidationError as e:
        await message.answer(e.message)

@router.message(Registration.gender)
async def fill_gender(message: Message, state: FSMContext):
    try:
        gender = GenderValidator().validate(message)
        await state.update_data(gender=gender)
        await state.set_state(Registration.description)
        await message.answer(msg.ABOUT_YOU, reply_markup=ReplyKeyboardRemove())
    except ValidationError as e:
        await message.answer(e.message, reply_markup=GENDERS)

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
        await state.clear()
        await message.answer(msg.REGISTER_IS_OVER)
    else:
        await message.answer(msg.MUST_SEND_PHOTO)
