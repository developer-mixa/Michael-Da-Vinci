from typing import TypedDict

class BaseAcquaintanceData(TypedDict):
    user_id: int
    action: str


class SearchAcquaintanceData(BaseAcquaintanceData):
    pass


class LikeUserData(BaseAcquaintanceData):
    liked_user_id: int