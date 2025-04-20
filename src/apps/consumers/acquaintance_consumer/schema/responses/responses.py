import enum
from typing import TypedDict

from src.apps.consumers.common.user_data import UserData


class AcquaintanceResponseStatus(enum.Enum):
    NON_REGISTERED = 1
    NOT_FOUND = 2
    FOUND = 3
    PROFILE_MUST_BE_ACTIVATED = 4
    UNEXCEPTED_ERROR = 5

    def serialize(self) -> int:
        return self.value

    @staticmethod
    def deserialize(number: int) -> 'AcquaintanceResponseStatus':
        return {
            1: AcquaintanceResponseStatus.NON_REGISTERED,
            2: AcquaintanceResponseStatus.NOT_FOUND,
            3: AcquaintanceResponseStatus.FOUND,
            4: AcquaintanceResponseStatus.PROFILE_MUST_BE_ACTIVATED,
        }.get(number, AcquaintanceResponseStatus.UNEXCEPTED_ERROR)


class LikedResponseStatus(enum.Enum):
    LIKE_SENT = 5
    MUTUALLY = 6
    UNEXCEPTED_ERROR = 4

    def serialize(self) -> int:
        return self.value

    @staticmethod
    def deserialize(number: int) -> 'LikedResponseStatus':
        if number == 5:
            return LikedResponseStatus.LIKE_SENT
        elif number == 6:
            return LikedResponseStatus.MUTUALLY
        else:
            return LikedResponseStatus.UNEXCEPTED_ERROR


class AcquaintanceResponse(TypedDict):
    response: int
    data: UserData | None


ACQUAINTANCE_UNEXCEPTED_ERROR = AcquaintanceResponse(
    response=AcquaintanceResponseStatus.UNEXCEPTED_ERROR.serialize(),
    data=None,
)

ACQUAINTANCE_NON_REGISTERED = AcquaintanceResponse(
    response=AcquaintanceResponseStatus.NON_REGISTERED.serialize(),
    data=None,
)

ACQUAINTANCE_NOT_FOUND = AcquaintanceResponse(
    response=AcquaintanceResponseStatus.NOT_FOUND.serialize(),
    data=None,
)

PROFILE_MUST_BE_ACTIVATED = AcquaintanceResponse(
    response=AcquaintanceResponseStatus.PROFILE_MUST_BE_ACTIVATED.serialize(),
    data=None,
)
