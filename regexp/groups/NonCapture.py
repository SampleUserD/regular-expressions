from .__types__ import Cursor, Status, Matchable, Groups

class NonCapture(Matchable):
  def __init__(self, expression: Matchable):
    self._expression = expression

  def match(self, cursor: Cursor, groups: Groups) -> Status:
    return self._expression.match(cursor, groups)