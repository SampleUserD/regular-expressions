from typing import Generic, TypeVar, Callable
from enum import Enum

from .Manager import Manager
from .Package import Package

EventType = TypeVar('EventType', bound=Enum)
PackageType = TypeVar('PackageType', bound=Package)

def delete_all_by(callback: Callable[[any], None], array: list[any]) -> None:
  index = 0

  while index < len(array):
    if callback(array[index]):
      array.pop(index)
      index -= 1

    index += 1

class Event(Generic[EventType, PackageType]):
  def __init__(self, type: EventType, package: PackageType):
    self.type = type
    self.package = package
    self.used: bool = False

  def mark_used(self) -> None:
    if not self.used:
      self.used = True

class Scheduler(Generic[EventType]):
  def __init__(self):
    self._manager = Manager()
    self._bus: list[Event[EventType, PackageType]] = []

  def _reuse_reserved_events(self, event_type: EventType):
    for event in self._bus:
      if (event.type.value == event_type.value) and (not event.used):
        self._manager.fire(event.type, event.package)
        event.mark_used()

  def _clean_garbage(self):
    delete_all_by(lambda x: x.used, self._bus)

  def on(self, event_type: EventType, callback: Callable[[PackageType], None]):
    self._manager.on(event_type, callback)
    self._clean_garbage()
    self._reuse_reserved_events(event_type)

  def fire(self, event_type: EventType, package: PackageType) -> None:
    self._bus.append(Event(event_type, package))