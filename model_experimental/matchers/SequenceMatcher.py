from .CharacterMatcher import CharacterMatcher

class SequenceMatcher(CharacterMatcher):
  def __init__(self, characters: list[str]):
    self._characters = characters

  def condition(self, character: str) -> bool:
    return character in self._characters
