from typing import Generic, TypeVar

from .Command import Command
from .Dependency import Dependency

Dependencies = TypeVar('Dependencies', bound=Dependency)
ReturnType = TypeVar('ReturnType')

class ImmediateExecutor(Generic[Dependencies]):
  def apply(self, command: Command) -> ReturnType:
    raise Exception('You should implement ImmediateExecutor.apply(Command)')