from typing import TypedDict

from fastapi import Query

from popug_sdk.constants import DEFAULT_PAGE_SIZE


class PaginationDict(TypedDict):
    page: int
    page_size: int
    count: int


class BasePagination:
    def __init__(
        self,
        page: int = Query(1, ge=1),
        page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1),
    ) -> None:
        self._page = page
        self._page_size = page_size

    @property
    def limit(self) -> int:
        return self._page_size

    @property
    def offset(self) -> int:
        return (self._page - 1) * self._page_size

    def get_params(self, count: int) -> dict[str, PaginationDict]:
        raise NotImplementedError


class PagePagination(BasePagination):
    def get_params(self, count: int) -> dict[str, PaginationDict]:
        return {
            "pagination": {
                "page": self._page,
                "page_size": self._page_size,
                "count": count,
            }
        }
