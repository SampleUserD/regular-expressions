from .__packages__ import executor, Dependency
from .events import Types, CursorMovePackage

class MoveCursor(executor.Command[Dependency]):
  def execute(self, dependencies: Dependency) -> None:
    package = CursorMovePackage(character=dependencies.cursor.current, index=dependencies.cursor.index)

    dependencies.scheduler.fire(Types.CURSOR_MOVE, package)
    dependencies.cursor.next()