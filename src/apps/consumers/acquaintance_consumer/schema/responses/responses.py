import enum
from typing import  TypedDict
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
    def deserialize(number: int):
        if number == 1:
            return AcquaintanceResponseStatus.NON_REGISTERED
        elif number == 2:
            return AcquaintanceResponseStatus.NOT_FOUND
        elif number == 3:
            return AcquaintanceResponseStatus.FOUND
        elif number == 4:
            return AcquaintanceResponseStatus.PROFILE_MUST_BE_ACTIVATED
        else:
            return AcquaintanceResponseStatus.UNEXCEPTED_ERROR


class LikedResponseStatus(enum.Enum):
    LIKE_SENT = 5
    MUTUALLY = 6
    UNEXCEPTED_ERROR = 4

    def serialize(self) -> int:
        return self.value

    @staticmethod
    def deserialize(number: int):
        if number == 5:
            return LikedResponseStatus.LIKE_SENT
        elif number == 6:
            return LikedResponseStatus.MUTUALLY
        else:
            return LikedResponseStatus.UNEXCEPTED_ERROR

class AcquaintanceResponse(TypedDict):
    response: AcquaintanceResponseStatus
    data: UserData | None = None


ACQUAINTANCE_UNEXCEPTED_ERROR = AcquaintanceResponse(response=AcquaintanceResponseStatus.UNEXCEPTED_ERROR.serialize())
ACQUAINTANCE_NON_REGISTERED = AcquaintanceResponse(response=AcquaintanceResponseStatus.NON_REGISTERED.serialize())
ACQUAINTANCE_NOT_FOUND = AcquaintanceResponse(response=AcquaintanceResponseStatus.NOT_FOUND.serialize())
PROFILE_MUST_BE_ACTIVATED = AcquaintanceResponse(response=AcquaintanceResponseStatus.PROFILE_MUST_BE_ACTIVATED.serialize())