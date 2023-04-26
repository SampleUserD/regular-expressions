from dataclasses import dataclass

from .__packages__ import memory, cursor, scheduler
from .__packages__ import executor

@dataclass(init=True, frozen=False)
class Dependency(executor.Dependency):
  cursor: cursor.Cursor
  memory: memory.Memory
  scheduler: scheduler.Scheduler