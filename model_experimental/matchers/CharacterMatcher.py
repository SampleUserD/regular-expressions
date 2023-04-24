from .__package__ import Matchable, Status, Executor, cursor

class CharacterMatcher(Matchable):
  def condition(self, character: str) -> bool:
    raise Exception('You should implement CharacterMatcher.condition(cursor: Cursor)')

  def match(self, executor: Executor) -> Status:
    if cursor.done(executor): return Status.STOP
    if self.condition(cursor.current(executor)):
      cursor.next(executor)
      return Status.TRUE

    return Status.FALSE