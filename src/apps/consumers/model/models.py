import enum
from datetime import date

from sqlalchemy import BigInteger, Enum, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.apps.common.models.meta import Base
from src.apps.common.models.uuid_mixin import UUIDMixin

MAX_NAME_LEN = 128
MAX_DESCRIPTION_LEN = 1024


class UserStatus(enum.Enum):
    ACTIVE = 1
    NO_ACTIVE = 2


class Gender(enum.Enum):
    GIRL = 1
    MAN = 2


class User(Base, UUIDMixin):
    __tablename__ = 'user'

    name: Mapped[str] = mapped_column(String(MAX_NAME_LEN))
    description: Mapped[str] = mapped_column(String(MAX_DESCRIPTION_LEN))
    dateOfBirth: Mapped[date]
    telegram_id = mapped_column(BigInteger, unique=True)
    status = mapped_column(Enum(UserStatus))
    gender = mapped_column(Enum(Gender))

    __table_args__ = (UniqueConstraint('telegram_id', name='uq_user_telegram_id'),)
