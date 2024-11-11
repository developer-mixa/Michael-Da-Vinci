from src.apps.consumers.model.models import User, UserStatus
from src.apps.consumers.register_consumer.schema.registration import RegistrationData

from src.core.utils.date import str_to_date

def user_from_reg_data(reg_data: RegistrationData) -> User:
    return User(
        name=reg_data['name'],
        description=reg_data['description'],
        image=reg_data['image'],
        dateOfBirth=str_to_date(reg_data['age']),
        telegram_id=reg_data['user_id'],
        status=UserStatus.NO_ACTIVE
    )
