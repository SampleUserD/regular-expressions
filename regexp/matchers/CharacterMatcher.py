from .__types__ import Cursor, Status, Matchable, Groups

class CharacterMatcher(Matchable):
  def condition(self, cursor: Cursor) -> bool:
    raise Exception('You should implement CharacterMatcher.condition(cursor: Cursor)')

  def match(self, cursor: Cursor, groups: Groups) -> Status:
    if cursor.done: return Status.STOP
    if self.condition(cursor):
      cursor.next()
      return Status.TRUE

    return Status.FALSE