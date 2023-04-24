from .__packages__ import executor, Dependency
from .Type import Type

from .MoveCursor import MoveCursor
from .ScreenshotCursorChange import ScreenshotCursorChange
from .CheckCursorDone import CheckCursorDone
from .GetCursorCurrentCharacter import GetCursorCurrentCharacter

def create(command_type: Type, arguments: list[any]) -> executor.Command[Dependency]:
  if command_type.value == Type.MOVE_CURSOR.value:
    return MoveCursor()
  elif command_type.value == Type.SCREENSHOT_CURSOR_CHANGE.value:
    return ScreenshotCursorChange(arguments[0])
  elif command_type.value == Type.CHECK_IF_CURSOR_DONE.value:
    return CheckCursorDone()
  elif command_type.value == Type.GET_CURSOR_CURRENT_CHARACTER.value:
    return GetCursorCurrentCharacter()