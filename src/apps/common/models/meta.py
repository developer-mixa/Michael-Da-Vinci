from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import MetaData
from src.apps.common.models.config import DEFAULT_SCHEMA

metadata = MetaData(schema=DEFAULT_SCHEMA)

class Base(DeclarativeBase):
    metadata = metadata
    __table_args__ = {'schema': DEFAULT_SCHEMA}