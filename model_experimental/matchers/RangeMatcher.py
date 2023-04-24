from .CharacterMatcher import CharacterMatcher

class RangeMatcher(CharacterMatcher):
  def __init__(self, start: str, end: str):
    self._range = range(ord(start), ord(end) + 1)

  def condition(self, character: str) -> bool:
    return ord(character) in self._range