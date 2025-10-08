from typing import TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T", bound=DeclarativeBase)


def map_model(target: T, source: BaseModel, exclude_unset: bool = True) -> T:
    """
    Maps fields from a Pydantic model to an existing SQLAlchemy model instance.

    - Only updates attributes that exist on the SQLAlchemy model.
    - Optionally ignores unset fields in the Pydantic model (useful for PATCH-like behavior).

    :param target: SQLAlchemy model instance to update
    :param source: Pydantic model instance containing incoming data
    :param exclude_unset: If True, only updates fields that were explicitly set
    :return: Updated SQLAlchemy model instance
    """
    source_data = source.model_dump(exclude_unset=exclude_unset)

    for field, value in source_data.items():
        if hasattr(target, field):
            setattr(target, field, value)

    return target
