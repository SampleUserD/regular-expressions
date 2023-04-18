from .__types__ import Cursor, Status, Matchable, Groups

class SubstringMatcher(Matchable):
  def __init__(self, substring: str):
    self._substring = substring

  def match(self, cursor: Cursor, groups: Groups) -> Status:
    if cursor.index >= cursor.length: return Status.STOP
    if len(self._substring) > cursor.length: return Status.STOP

    for character in self._substring:
      if cursor.current == character: cursor.next()
      else: return Status.FALSE

    return Status.TRUE