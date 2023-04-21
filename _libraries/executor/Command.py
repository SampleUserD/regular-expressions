from typing import Generic, TypeVar

from .Dependency import Dependency

Dependencies = TypeVar('Dependencies', bound=Dependency)

class Command(Generic[Dependencies]):
  def execute(self, dependencies: Dependencies) -> None:
    raise Exception('You should implement Command.execute(Context)')