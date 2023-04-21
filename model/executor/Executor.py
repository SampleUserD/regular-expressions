from .__packages__ import executor

from .Dependency import Dependency

class Executor(executor.Executor[Dependency]):
  def __init__(self, dependency: Dependency):
    self._dependency = dependency
    self._commandPool: list[executor.Command[Dependency]] = []

  def use(self, command: executor.Command[Dependency]) -> None:
    self._commandPool.append(command)

  def execute(self) -> None:
    for command in self._commandPool:
      command.execute(self._dependency)