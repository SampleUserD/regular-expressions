from .__types__ import Matchable, Cursor, Groups, Status

from .SubstringMatcher import SubstringMatcher

class ReferenceMatcher(Matchable):
  def __init__(self, name: str):
    self._name = name

  def match(self, cursor: Cursor, groups: Groups) -> Status:
    matcher = SubstringMatcher(groups.get(self._name))
    return matcher.match(cursor, groups)