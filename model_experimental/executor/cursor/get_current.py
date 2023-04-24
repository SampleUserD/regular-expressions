from .__packages__ import Type, create
from .__packages__ import executor

def get_current(executor: executor.ImmediateExecutor) -> str:
  return executor.apply(create(Type.GET_CURSOR_CURRENT_CHARACTER, []))