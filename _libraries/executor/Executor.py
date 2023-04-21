from typing import Generic, TypeVar

from .Command import Command
from .Dependency import Dependency

Dependencies = TypeVar('Dependencies', bound=Dependency)

class Executor(Generic[Dependencies]):
  def use(self, command: Command) -> None:
    raise Exception('You should implement Driver.use(Command)')

  def execute(self) -> None:
    raise Exception('You should implement Driver.execute()')