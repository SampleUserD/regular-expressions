from .CharacterMatcher import CharacterMatcher

class NonSequenceMatcher(CharacterMatcher):
  def __init__(self, characters: list[str]):
    self._characters = characters

  def condition(self, character: str) -> bool:
    return character not in self._characters
