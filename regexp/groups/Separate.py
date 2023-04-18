from .__types__ import Cursor, Status, Matchable, Groups

class Separate(Matchable):
  def __init__(self, expression: Matchable):
    self._expression = expression

  def match(self, cursor: Cursor, groups: Groups) -> Status:
    groups.create_frame()
    status = self._expression.match(cursor, groups)

    if status == Status.TRUE:
      return status

    groups.remove_frame()

    return status
