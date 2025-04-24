import enum
from datetime import date, datetime
from typing import Any, Dict

from sqlalchemy import UUID, BigInteger, Enum, ForeignKey, String, UniqueConstraint
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
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String(MAX_NAME_LEN))
    description: Mapped[str] = mapped_column(String(MAX_DESCRIPTION_LEN))
    date_of_birth: Mapped[date]
    telegram_id = mapped_column(BigInteger, unique=True)
    status = mapped_column(Enum(UserStatus, name='user_status'))
    gender = mapped_column(Enum(Gender, name='gender'))

    __table_args__ = (UniqueConstraint('telegram_id', name='uq_user_telegram_id'),)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'date_of_birth': self.date_of_birth.isoformat(),
            'telegram_id': self.telegram_id,
            'status': self.status.value,
            'gender': self.gender.value
        }

    @staticmethod
    def from_dict(data: dict) -> "User":
        return User(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            date_of_birth=date.fromisoformat(data['date_of_birth']),
            telegram_id=data['telegram_id'],
            status=UserStatus(data['status']),
            gender=Gender(data['gender'])
        )


class Like(Base):
    __tablename__ = 'likes'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    target_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    sender_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
