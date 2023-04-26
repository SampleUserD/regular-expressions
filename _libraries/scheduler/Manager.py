from typing import Generic, TypeVar, Callable
from enum import Enum

from .Package import Package

EventType = TypeVar('EventType', bound=Enum)
PackageType = TypeVar('PackageType', bound=Package)

class EventHandler(Generic[EventType, PackageType]):
  def __init__(self, event_type: EventType, handler: Callable[[PackageType], None]):
    self.event_type = event_type
    self.handler = handler
    self.used: bool = False

  def mark_used(self) -> None:
    if not self.used:
      self.used = True

def delete_all_by(callback: Callable[[any], None], array: list[any]) -> None:
  index = 0

  while index < len(array):
    if callback(array[index]):
      array.pop(index)
      index -= 1

    index += 1

class Manager(Generic[EventType]):
  def __init__(self):
    self._handlers: list[EventHandler[EventType, PackageType]] = []

  def _clean_garbage(self):
    delete_all_by(lambda x: x.used, self._handlers)

  def on(self, event_type: EventType, callback: Callable[[PackageType], None]):
    self._handlers.append(EventHandler(event_type, callback))
    self._clean_garbage()

  def fire(self, event_type: EventType, package: PackageType):
    to_delete: list[int] = []

    for index in range(0, len(self._handlers)):
      handler = self._handlers[index]

      if handler.event_type.value == event_type.value:
        handler.handler(package)
        to_delete.append(index)

    for index in to_delete:
      self._handlers[index].mark_used()
