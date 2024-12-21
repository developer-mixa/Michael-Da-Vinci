from aiogram.fsm.state import State, StatesGroup


class UpdateProfile(StatesGroup):
    update_field_name = State()
    update_field_value = State()
