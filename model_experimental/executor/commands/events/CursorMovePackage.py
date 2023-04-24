from dataclasses import dataclass

from .__packages__ import event

@dataclass(init=True)
class CursorMovePackage(event.Package):
  character: str
  index: int