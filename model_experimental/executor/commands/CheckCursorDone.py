from .__packages__ import executor, Dependency

class CheckCursorDone(executor.Command[Dependency]):
  def execute(self, dependencies: Dependency) -> bool:
    return dependencies.cursor.done