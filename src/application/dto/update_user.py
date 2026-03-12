"""DTO for update user state use case."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UpdateUserInput:
    user_id: int
    name: Optional[str] = None
    age: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None  # True=active, False=inactive
    image: Optional[str] = None

