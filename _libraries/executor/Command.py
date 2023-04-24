from typing import Generic, TypeVar

from .Dependency import Dependency

Dependencies = TypeVar('Dependencies', bound=Dependency)
ReturnType = TypeVar('ReturnType')

class Command(Generic[Dependencies]):
  def execute(self, dependencies: Dependencies) -> ReturnType:
    raise Exception('You should implement Command.execute(Context)')