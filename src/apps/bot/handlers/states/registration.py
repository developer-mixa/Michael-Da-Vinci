from aiogram.fsm.state import StatesGroup, State

class Registration(StatesGroup):
    accept_privacy_policy = State()
    age = State()
    gender = State()
    location = State()
    name = State()
    description = State()
    image = State()