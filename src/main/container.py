"""
Composition Root — DI container.

All infrastructure components are wired together here.
Use cases receive their dependencies via constructor injection.
Presentation layer gets use cases and producers from this module.
"""

from config.settings import settings

# --- Infrastructure: Redis Cache ---
from src.infrastructure.redis.cache import RedisCache

cache = RedisCache(
    host=settings.REDIS_HOST,
    port=int(settings.REDIS_PORT),
    password=settings.REDIS_PASSWORD,
)

# --- Infrastructure: Database Session ---
from src.infrastructure.database.session import async_session

# --- Infrastructure: Repositories ---
from src.infrastructure.database.user_repository import SqlAlchemyUserRepository
from src.infrastructure.database.like_repository import SqlAlchemyLikeRepository
from src.infrastructure.database.acquaintance_repository import SqlAlchemyAcquaintanceRepository

user_repository = SqlAlchemyUserRepository(async_session)
like_repository = SqlAlchemyLikeRepository(async_session)
acquaintance_repository = SqlAlchemyAcquaintanceRepository(async_session, cache, like_repository)

# --- Infrastructure: File Storage ---
from src.infrastructure.storage.s3_client import S3FileStorage

file_storage = S3FileStorage(
    endpoint=f'{settings.MINIO_HOST}:9000',
    access_key=settings.MINIO_USER,
    secret_key=settings.MINIO_PASSWORD,
    bucket_name='user-images',
)

# --- Application: Use Cases ---
from src.application.use_cases.register_user import RegisterUserUseCase
from src.application.use_cases.search_acquaintance import SearchAcquaintanceUseCase
from src.application.use_cases.like_user import LikeUserUseCase
from src.application.use_cases.update_user_state import UpdateUserStateUseCase

register_user_use_case = RegisterUserUseCase(user_repository, file_storage)
search_acquaintance_use_case = SearchAcquaintanceUseCase(acquaintance_repository, file_storage)
like_user_use_case = LikeUserUseCase(user_repository, like_repository)
update_user_state_use_case = UpdateUserStateUseCase(user_repository)

# --- Presentation: Consumers ---
from src.presentation.consumers.registration_consumer import RegistrationConsumer
from src.presentation.consumers.acquaintance_consumer import AcquaintanceConsumer
from src.presentation.consumers.user_state_consumer import UserStateConsumer


def create_registration_consumer() -> RegistrationConsumer:
    return RegistrationConsumer(settings.rabbit_url, register_user_use_case)


def create_acquaintance_consumer() -> AcquaintanceConsumer:
    return AcquaintanceConsumer(settings.rabbit_url, search_acquaintance_use_case, like_user_use_case)


def create_user_state_consumer() -> UserStateConsumer:
    return UserStateConsumer(settings.rabbit_url, update_user_state_use_case)


# --- Producers (used by bot handlers via RabbitMQ) ---
# These are the same consumer classes used as producers (context manager pattern)

def get_registration_producer() -> RegistrationConsumer:
    return create_registration_consumer()


def get_acquaintance_producer() -> AcquaintanceConsumer:
    return create_acquaintance_consumer()


def get_user_state_producer() -> UserStateConsumer:
    return create_user_state_consumer()

