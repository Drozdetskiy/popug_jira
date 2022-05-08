from collections import deque
from typing import (
    Generic,
    TypeVar,
)

from sqlalchemy.orm import Session

RepoData = TypeVar("RepoData")


class NoContextError(Exception):
    pass


class BaseRepo(Generic[RepoData]):
    def __init__(
        self,
        session: Session,
    ):
        self._session = session
        self._context_stack: deque[RepoData] = deque()

    @property
    def is_empty(self) -> bool:
        return not self._context_stack

    def status(self) -> RepoData:
        self._session.flush()

        return self.get()

    def apply(self) -> RepoData:
        self._session.commit()

        return self.get()

    def get(self) -> RepoData:
        if not self._context_stack:
            raise NoContextError

        return self._context_stack.pop()

    def first(self) -> RepoData | None:
        if self._context_stack:
            return self._context_stack.pop()

        return None

    def _append_context(self, context: RepoData) -> None:
        if context is not None:
            self._context_stack.append(context)
