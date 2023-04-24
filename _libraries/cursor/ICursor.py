from typing import Generic, TypeVar

Iterable = TypeVar('Iterable')

class ICursor(Generic[Iterable]):
  def __init__(self, string: list[Iterable]):
    self._string = string
    self._index = 0

  def next(self) -> None:
    if not self.done: self._index += 1

  @property
  def current(self) -> Iterable: return self._string[self._index]

  @property
  def index(self) -> int: return self._index

  @property
  def length(self) -> int: return len(self._string)

  @property
  def done(self) -> bool: return self.index >= self.length