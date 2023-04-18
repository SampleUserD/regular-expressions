from .__types__ import Cursor
from .__types__ import Status

from .Matchable import Matchable
from .Groups import Groups

class Expression(Matchable):
  def __init__(self, expressions: list[Matchable]):
    self._expressions = expressions

  def match(self, cursor: Cursor, groups: Groups) -> Status:
    cursor.save()

    for expression in self._expressions:
      status = expression.match(cursor, groups)

      if status in [Status.FALSE, Status.STOP]:
        cursor.restore()
        return status

    cursor.discard()

    return Status.TRUE