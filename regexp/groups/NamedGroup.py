from .__types__ import Groups, Matchable

from .Group import Group

class NamedGroup(Group):
  def __init__(self, name: str, expressions: list[Matchable]):
    super().__init__(expressions)
    self._name = name

  def add_group(self, string: str, groups: Groups) -> None:
    groups.add_named(self._name, string)
