from typing import Generic, TypeVar

from .Frame import Frame

Value = TypeVar('Value')

class Memory(Generic[Value]):
  _frames: list[Frame[Value]] = [Frame[Value]()]

  def add_frame(self, frame: Frame[Value]) -> None: self._frames.append(frame)

  def add(self, value: Value, **kwargs) -> None: self.last_frame.add(value, **kwargs)
  def get(self, name: str) -> str: return self.last_frame.get(name)

  @property
  def last_frame(self) -> Frame[Value]: return self._frames[len(self._frames) - 1]

  @property
  def reserves(self): return map(lambda frame: frame.group, self._frames)