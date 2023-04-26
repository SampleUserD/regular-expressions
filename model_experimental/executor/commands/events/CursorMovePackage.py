from dataclasses import dataclass

from .__packages__ import scheduler

@dataclass(init=True)
class CursorMovePackage(scheduler.Package):
  character: str
  index: int