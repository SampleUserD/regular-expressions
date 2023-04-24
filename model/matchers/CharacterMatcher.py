from .__types__ import Cursor, Status, Matchable, Groups

class CharacterMatcher(Matchable):
  def meets_condition(self, character: str) -> bool:
    raise Exception('You should implement CharacterMatcher.meets_condition(cursor: Cursor)')

  def match(self, cursor: Cursor, groups: Groups) -> Status:
    if cursor.done: return Status.STOP
    if self.meets_condition(cursor.current):
      cursor.next()
      return Status.TRUE

    return Status.FALSE