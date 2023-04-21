from .__types__ import Cursor, Status, Matchable, Groups

class Or(Matchable):
  def __init__(self, expressions: list[Matchable]):
    self._expressions = expressions

  def match(self, cursor: Cursor, groups: Groups) -> Status:
    for expression in self._expressions:
      status = expression.match(cursor, groups)

      if status in [status.TRUE, status.STOP]:
        return status

    return Status.FALSE