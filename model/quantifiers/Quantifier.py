from .__types__ import Cursor, Status, Matchable, Groups

class Quantifier(Matchable):
  def __init__(self, expression: Matchable):
    self._expression = expression

  def get_status_from_count(self, count: int) -> Status:
    raise Exception('You should implement get_status_from_count(count: int)')

  def match(self, cursor: Cursor, groups: Groups) -> Status:
    count = 0

    while (not cursor.done) and (self._expression.match(cursor, groups) not in [Status.STOP, Status.FALSE]):
      count += 1

    return self.get_status_from_count(count)
