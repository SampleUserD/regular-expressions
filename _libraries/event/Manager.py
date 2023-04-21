from typing import Generic, TypeVar, Callable
from enum import Enum

from .Package import Package
EventType = TypeVar('EventType', bound=Enum)
PackageType = TypeVar('PackageType', bound=Package)

class Manager(Generic[EventType]):
  def __init__(self):
    self._handlers: list[list[EventType, Callable[[PackageType], None], bool]] = []

  def _delete_used_handlers(self):
    index = 0

    while index < len(self._handlers):
      if self._handlers[index][2]:
        self._handlers.pop(index)
        index -= 1

      index += 1

  def on(self, event_type: EventType, callback: Callable[[PackageType], None]):
    self._handlers.append([event_type, callback, False])
    self._delete_used_handlers()

  def fire(self, event_type: EventType, package: PackageType):
    to_delete: list[int] = []

    for index in range(0, len(self._handlers)):
      handler = self._handlers[index]
      handler_type = handler[0]
      handler_callback = handler[1]

      if handler_type.value == event_type.value:
        handler_callback(package)
        to_delete.append(index)

    for index in to_delete:
      self._handlers[index][2] = True
