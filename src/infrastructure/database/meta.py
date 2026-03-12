"""SQLAlchemy declarative base and metadata."""

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import MetaData

DEFAULT_SCHEMA = 'public'
metadata = MetaData(schema=DEFAULT_SCHEMA)


class Base(DeclarativeBase):
    metadata = metadata
    __table_args__ = {'schema': DEFAULT_SCHEMA}

