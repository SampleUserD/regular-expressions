from .__types__ import Cursor
from .CharacterMatcher import CharacterMatcher

class RangeMatcher(CharacterMatcher):
  def __init__(self, start: str, end: str):
    self._range = range(ord(start), ord(end) + 1)

  def condition(self, cursor: Cursor) -> bool:
    return ord(cursor.current) in self._range