from .__types__ import Cursor
from .CharacterMatcher import CharacterMatcher

class SequenceMatcher(CharacterMatcher):
  def __init__(self, characters: list[str]):
    self._characters = characters

  def meets_condition(self, character: str) -> bool:
    return character in self._characters
