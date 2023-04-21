from dataclasses import dataclass
from typing import Generic, TypeVar
from enum import Enum

from .Package import Package

EventType = TypeVar('EventType', bound=Enum)
PackageType = TypeVar('PackageType', bound=Package)

@dataclass()
class Event(Generic[EventType, PackageType]):
  type: EventType
  package: PackageType