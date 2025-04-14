import enum
from typing import  TypedDict
from src.apps.consumers.common.user_data import UserData


class AcquaintanceResponseStatus(enum.Enum):
    NON_REGISTERED = 1
    NOT_FOUND_USERS = 2
    FOUND_USERS = 3
    UNEXCEPTED_ERROR = 4

    def serialize(self) -> int:
        return self.value
    
    @staticmethod
    def deserialize(number: int):
        if number == 1:
            return AcquaintanceResponseStatus.NON_REGISTERED
        elif number == 2:
            return AcquaintanceResponseStatus.NOT_FOUND_USERS
        elif number == 3:
            return AcquaintanceResponseStatus.FOUND_USERS
        else:
            return AcquaintanceResponseStatus.UNEXCEPTED_ERROR


class AcquaintanceResponse(TypedDict):
    response: AcquaintanceResponseStatus
    data: UserData | None = None

