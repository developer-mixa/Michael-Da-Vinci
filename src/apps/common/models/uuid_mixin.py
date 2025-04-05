"""Module with UUIDMixin."""
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column


class UUIDMixin:
    """Mixin which add 'id' column to the table."""

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)