from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    accept_privacy_policy = State()
    age = State()
    gender = State()
    name = State()
    description = State()
    image = State()
