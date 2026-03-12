"""Domain entity: Like."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class Like:
    sender_user_id: UUID
    target_user_id: UUID
    id: int | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)

