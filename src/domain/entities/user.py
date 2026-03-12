"""Domain entity: User."""

import enum
from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4


class UserStatus(enum.Enum):
    ACTIVE = 1
    NO_ACTIVE = 2


class Gender(enum.Enum):
    GIRL = 1
    MAN = 2


@dataclass
class User:
    name: str
    description: str
    date_of_birth: date
    telegram_id: int
    status: UserStatus
    gender: Gender
    id: UUID = field(default_factory=uuid4)

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    @property
    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE

