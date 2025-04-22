from typing import TypedDict

from src.apps.consumers.model.models import Gender, User


class UserData(TypedDict):
    name: str
    age: str
    gender: str
    description: str
    image: bytes
    user_id: int

    @staticmethod
    def from_db_user(user: User, user_image: bytes) -> 'UserData':
        return {
            'name': user.name,
            'age': str(user.date_of_birth),
            'description': user.description,
            'gender': 'Девушка' if user.gender == Gender.GIRL else 'Парень',
            'image': user_image,
            'user_id': user.telegram_id,
        }
