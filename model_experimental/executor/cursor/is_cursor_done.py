from .__packages__ import Type, create
from .__packages__ import executor

def is_cursor_done(executor: executor.ImmediateExecutor) -> bool:
  return executor.apply(create(Type.CHECK_IF_CURSOR_DONE, []))