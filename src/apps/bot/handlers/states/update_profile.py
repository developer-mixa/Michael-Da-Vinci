from aiogram.fsm.state import StatesGroup, State

class UpdateProfile(StatesGroup):
    update_field = State()