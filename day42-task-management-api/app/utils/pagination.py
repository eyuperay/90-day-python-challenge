from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20


def paginate(items: list, page: int = 1, page_size: int = 20):
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end]