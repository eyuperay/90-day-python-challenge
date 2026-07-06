from typing import Optional
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20

class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int
    total_pages: int

def paginate(query, pagination: PaginationParams):
    total = query.count()
    items = query.offset((pagination.page - 1) * pagination.page_size) \
                 .limit(pagination.page_size) \
                 .all()
    return {
        "items": items,
        "total": total,
        "page": pagination.page,
        "page_size": pagination.page_size,
        "total_pages": (total + pagination.page_size - 1) // pagination.page_size
    }