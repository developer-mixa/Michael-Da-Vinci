from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F
from ..states.registration import Registration
from .router import router

@router.message(F.text == "/registration")
async def start_registration(message: Message, state: FSMContext):
    await state.set_state(Registration.accept_privacy_policy)
    await message.answer('Продолжая, вы принимаете пользовательское соглашение и политику конфидициальности.')

@router.message(Registration.accept_privacy_policy)
async def fill_name(message: Message, state: FSMContext):
    await state.update_data(accept_privacy_policy=message.text)
    await state.set_state(Registration.name)
    await message.answer('Как тебя зовут?')

@router.message(Registration.name)
async def fill_age(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Registration.age)
    await message.answer('Сколько тебе лет?')

@router.message(Registration.age)
async def fill_gender(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Registration.gender)
    await message.answer('Какой у тебя пол?')

@router.message(Registration.gender)
async def fill_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(Registration.description)
    await message.answer('Расскажи о себе')

@router.message(Registration.description)
async def fill_gender(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Registration.location)
    await message.answer('Из какого ты города?')

@router.message(Registration.location)
async def fill_location(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(Registration.image)
    await message.answer('Теперь пришли своё фото, его будут видеть другие пользователи')

@router.message(Registration.image)
async def fill_image(message: Message, state: FSMContext):
    await state.update_data(image=message.text)
    await state.clear()
    await message.answer('Регистрация завершена!')
