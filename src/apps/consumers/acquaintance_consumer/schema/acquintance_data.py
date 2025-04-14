from typing import TypedDict

class BaseAcquaintanceData(TypedDict):
    user_id: int
    action: str


class SearchAcquaintanceData(BaseAcquaintanceData):
    pass

class MutualityData(TypedDict):
    liked_user_id: int
    sender_user_id: int

class LikeUserData(BaseAcquaintanceData, MutualityData):
    liked_user_id: int