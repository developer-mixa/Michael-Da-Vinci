from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, BigInteger, Enum
import enum

from src.apps.common.models.uuid_mixin import UUIDMixin
from src.apps.common.models.meta import Base

from datetime import date

MAX_NAME_LEN = 128
MAX_DESCRIPTION_LEN = 1024

class UserStatus(enum.Enum):
    ACTIVE = 1
    NO_ACTIVE = 2

class User(Base, UUIDMixin):
    __tablename__ = 'user'

    name: Mapped[str] = mapped_column(String(MAX_NAME_LEN))
    description: Mapped[str] = mapped_column(String(MAX_DESCRIPTION_LEN))
    image: Mapped[str] = mapped_column(Text)
    dateOfBirth: Mapped[date]
    telegram_id = mapped_column(BigInteger)
    status = mapped_column(Enum(UserStatus))
