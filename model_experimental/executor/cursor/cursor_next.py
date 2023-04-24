from .__packages__ import Type, create
from .__packages__ import executor

def cursor_next(executor: executor.ImmediateExecutor) -> None:
  executor.apply(create(Type.MOVE_CURSOR, []))