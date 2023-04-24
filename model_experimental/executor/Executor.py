from typing import TypeVar

from .__packages__ import executor

from .Dependency import Dependency

ReturnType = TypeVar('ReturnType')

class Executor(executor.ImmediateExecutor[Dependency]):
  def __init__(self, dependency: Dependency):
    self._dependency = dependency

  def apply(self, command: executor.Command[Dependency]) -> ReturnType:
    return command.execute(self._dependency)