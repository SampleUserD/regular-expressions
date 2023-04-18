from .__types__ import Cursor, Status, Matchable, Groups

class AnySymbol(Matchable):
  def match(self, cursor: Cursor, groups: Groups) -> Status:
    if cursor.index >= cursor.length: return Status.STOP

    cursor.next()
    return Status.TRUE