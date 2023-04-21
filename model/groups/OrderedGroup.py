from .__types__ import Groups

from .Group import Group

class OrderedGroup(Group):
  def add_group(self, string: str, groups: Groups) -> None:
    groups.add_ordered(string)
