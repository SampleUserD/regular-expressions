from .__types__ import Cursor
from .CharacterMatcher import CharacterMatcher

class SequenceMatcher(CharacterMatcher):
  def __init__(self, characters: list[str]):
    self._characters = characters

  def condition(self, cursor: Cursor) -> bool:
    return cursor.current in self._characters
