"""DTO for acquaintance / matching use cases."""

import enum
from dataclasses import dataclass
from typing import Optional


class AcquaintanceStatus(enum.Enum):
    FOUND = 3
    NOT_FOUND = 2
    NON_REGISTERED = 1
    PROFILE_MUST_BE_ACTIVATED = 4
    UNEXPECTED_ERROR = 5


class LikeStatus(enum.Enum):
    LIKE_SENT = 5
    MUTUALLY = 6
    UNEXPECTED_ERROR = 4


@dataclass(frozen=True)
class CandidateData:
    user_id: int
    name: str
    age: str
    gender: str
    description: str
    image: bytes


@dataclass(frozen=True)
class SearchResult:
    status: AcquaintanceStatus
    candidate: Optional[CandidateData] = None


@dataclass(frozen=True)
class LikeResult:
    status: LikeStatus
    liked_user_id: Optional[int] = None
    sender_user_id: Optional[int] = None

