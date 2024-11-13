from typing import TypedDict

class UpdateUserData(TypedDict):
    name: str | None
    age: str | None
    description: str | None
    location: str | None
    image: str | None
    user_id: int
    is_active: bool | None