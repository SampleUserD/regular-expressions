from typing import Generic, TypeVar, Callable
from enum import Enum

from .Manager import Manager
from .Package import Package

EventType = TypeVar('EventType', bound=Enum)
PackageType = TypeVar('PackageType', bound=Package)

class Scheduler(Generic[EventType]):
  def __init__(self):
    self._manager = Manager()
    self._bus: list[list[EventType, PackageType, bool]] = []

  def _delete_used_events(self):
    index = 0

    while index < len(self._bus):
      if self._bus[index][2]:
        self._bus.pop(index)
        index -= 1

      index += 1

  def _reuse_reserved_events(self, event_type: EventType):
    for event in self._bus:
      if (event[0].value == event_type.value) and (event[2] == False):
        self._manager.fire(event[0], event[1])
        event[2] = True

  def on(self, event_type: EventType, callback: Callable[[PackageType], None]):
    self._manager.on(event_type, callback)
    self._delete_used_events()
    self._reuse_reserved_events(event_type)

  def fire(self, event_type: EventType, package: PackageType) -> None:
    self._bus.append([event_type, package, False])