"""DTO for user registration use case."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RegistrationInput:
    user_id: int
    name: str
    age: str  # date string YYYY-MM-DD
    gender: str  # "Парень" / "Девушка"
    description: str
    image_base64: str
    accept_privacy_policy: str = ""

