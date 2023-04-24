from .__packages__ import executor, Dependency
from .events import Types

class ScreenshotCursorChange(executor.Command[Dependency]):
  def __init__(self, buffer: list[str]):
    self._buffer = buffer

  def execute(self, dependencies: Dependency) -> None:
    dependencies.scheduler.on(Types.CURSOR_MOVE, lambda package: self._buffer.append(package.character))