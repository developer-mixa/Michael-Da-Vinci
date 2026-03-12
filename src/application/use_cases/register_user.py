"""Use case: Register a new user."""

import base64
import io
import logging

from src.application.dto.registration import RegistrationInput
from src.domain.entities.user import Gender, User, UserStatus
from src.domain.exceptions import AlreadyRegisteredError
from src.domain.interfaces.file_storage import IFileStorage
from src.domain.interfaces.user_repository import IUserRepository
from src.domain.validators.age_validator import validate_date_of_birth

logger = logging.getLogger(__name__)


class RegisterUserUseCase:

    def __init__(self, user_repo: IUserRepository, file_storage: IFileStorage) -> None:
        self._user_repo = user_repo
        self._file_storage = file_storage

    async def execute(self, data: RegistrationInput) -> bool:
        """
        Register user.
        Returns True on success, False if already registered.
        """
        date_of_birth = validate_date_of_birth(data.age)
        gender = Gender.MAN if data.gender == 'Парень' else Gender.GIRL

        user = User(
            name=data.name,
            description=data.description,
            date_of_birth=date_of_birth,
            telegram_id=data.user_id,
            gender=gender,
            status=UserStatus.NO_ACTIVE,
        )

        try:
            await self._user_repo.create(user)
        except AlreadyRegisteredError:
            logger.info('User %s is already registered', data.user_id)
            return False

        image_bytes = base64.b64decode(data.image_base64)
        self._file_storage.upload_file(str(user.telegram_id), io.BytesIO(image_bytes))

        logger.info('User %s registered successfully', data.user_id)
        return True

