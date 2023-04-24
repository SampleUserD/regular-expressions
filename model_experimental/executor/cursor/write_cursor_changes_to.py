from .__packages__ import Type, create
from .__packages__ import executor

def write_cursor_changes_to(executor: executor.ImmediateExecutor, to: list[str]) -> None:
  executor.apply(create(Type.SCREENSHOT_CURSOR_CHANGE, [ to ]))