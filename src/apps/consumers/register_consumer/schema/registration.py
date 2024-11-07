from typing import TypedDict

class RegistrationData(TypedDict):
    accept_privacy_policy: str
    name: str
    age: str
    gender: str
    description: str
    location: str
    image: str
    user_id: str