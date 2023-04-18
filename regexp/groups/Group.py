from .__types__ import Cursor, Status, Matchable, Groups

from .NonCapture import NonCapture

class Group(Matchable):
  def __init__(self, expressions: list[Matchable]):
    self._expressions = expressions

  def add_group(self, string: str, groups: Groups) -> None:
    raise Exception('You should implement Group.add_group(string: str, groups: Groups)')

  def match(self, cursor: Cursor, groups: Groups) -> Status:
    start = cursor.index
    gaps = []

    def can_append_to_group(matcher: Matchable):
      return isinstance(matcher, NonCapture)

    def add_gap_index(cursor: Cursor, matcher: Matchable):
      if can_append_to_group(matcher):
        gaps.append(cursor.index)

    cursor.save()

    for expression in self._expressions:
      add_gap_index(cursor, expression)
      status = expression.match(cursor, groups)
      add_gap_index(cursor, expression)

      if status in [Status.FALSE, Status.STOP]:
        cursor.restore()
        return status

    indexes = [start] + gaps + [cursor.index]
    string = str()

    for index in range(0, len(indexes) - 1, 2):
      string += cursor.slice(indexes[index], indexes[index + 1])

    self.add_group(string, groups)
    cursor.discard()

    return Status.TRUE