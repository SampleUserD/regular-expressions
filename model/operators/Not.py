from .__types__ import Cursor, Status, Matchable, Groups

class Not(Matchable):
  def __init__(self, expression: Matchable):
    self._expression = expression

  def match(self, cursor: Cursor, groups: Groups) -> Status:
    status = self._expression.match(cursor, groups)

    if status == Status.FALSE:
      return Status.TRUE

    if status == Status.TRUE:
      return Status.FALSE

    return status