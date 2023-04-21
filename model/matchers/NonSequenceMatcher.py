from .__types__ import Cursor
from .CharacterMatcher import CharacterMatcher

class NonSequenceMatcher(CharacterMatcher):
  def __init__(self, characters: list[str]):
    self._characters = characters

  def condition(self, cursor: Cursor) -> bool:
    return cursor.current not in self._characters
