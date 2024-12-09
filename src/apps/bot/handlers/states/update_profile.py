from aiogram.fsm.state import StatesGroup, State

class UpdateProfile(StatesGroup):
    update_field_name = State()
    update_field_value = State()