from datetime import datetime
from typing import Any

from sqlalchemy import Column, and_, or_


def apply_date_range(query, column: Column, from_date: datetime | None, to_date: datetime | None):
    """Apply an inclusive date range filter to a SQLAlchemy query."""
    if from_date is not None:
        query = query.where(column >= from_date)
    if to_date is not None:
        query = query.where(column <= to_date)
    return query


def apply_search(query, *columns: Column, search: str | None):
    """Apply a case-insensitive LIKE search across one or more text columns."""
    if not search:
        return query
    pattern = f"%{search.lower()}%"
    conditions = [col.ilike(pattern) for col in columns]
    return query.where(or_(*conditions))
