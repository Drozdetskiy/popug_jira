from __future__ import annotations

from typing import (
    Generic,
    TypeVar,
)

from sqlalchemy.orm import Session

RepoData = TypeVar("RepoData")
RepoT = TypeVar("RepoT", bound="BaseRepo")  # type: ignore


class NoContextError(Exception):
    pass


class BaseRepo(Generic[RepoData]):
    def __init__(
        self,
        session: Session,
        context: RepoData | None = None,
    ):
        self._session = session
        self._context = context

    def __call__(self, context: RepoData | None) -> RepoT:
        self._context = context

        return self  # type: ignore

    @property
    def is_empty(self) -> bool:
        return self._context is None

    def status(self) -> RepoData:
        self._session.flush()

        return self.get()

    def apply(self) -> RepoData:
        result = self.get()
        self._session.commit()

        return result

    def get(self) -> RepoData:
        if self._context is None:
            raise NoContextError

        return self._context

    def context(self) -> RepoData | None:
        return self._context
