from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T", bound=DeclarativeBase)


def map_model(target: T, source: BaseModel, exclude_unset: bool = True) -> T:
    """
    Maps fields from a Pydantic model to a SQLAlchemy model instance.
    Only maps fields that exist on the target model.

    Args:
        target: SQLAlchemy model instance to update
        source: Pydantic model instance with new values

    Returns:
        Updated SQLAlchemy model instance
    """
    if not isinstance(target, DeclarativeBase):
        raise TypeError("Target must be a SQLAlchemy model instance")

    source_dict = source.model_dump()

    for field, value in source_dict.items():
        if hasattr(target, field):
            setattr(target, field, value)

    return target
