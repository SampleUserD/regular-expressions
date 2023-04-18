from .__types__ import Cursor, Status, Matchable, Groups

class TerminateSymbol(Matchable):
  def match(self, cursor: Cursor, groups: Groups) -> Status:
    return [Status.FALSE, Status.TRUE][int(cursor.index >= cursor.length)]