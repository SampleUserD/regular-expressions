from .__packages__ import executor, Dependency

class GetCursorCurrentCharacter(executor.Command[Dependency]):
  def execute(self, dependencies: Dependency) -> str:
    return dependencies.cursor.current