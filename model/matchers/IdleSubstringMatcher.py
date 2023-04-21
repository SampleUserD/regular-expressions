from .__types__ import Cursor, Status, Groups, Matchable

from .SubstringMatcher import SubstringMatcher

class IdleSubstringMatcher(Matchable):
  def __init__(self, substring: str):
    self._substring = substring

  def match(self, cursor: Cursor, groups: Groups) -> Status:
    cursor.save()

    matcher = SubstringMatcher(self._substring)
    status = matcher.match(cursor, groups)

    if status == Status.TRUE: cursor.discard()
    else: cursor.restore()

    return status