from .__types__ import Cursor, Status

from .Matchable import Matchable
from .Expression import Expression
from .Groups import Groups

class RegularExpression:
  def __init__(self, expressions: list[Matchable]):
    self._expressions = Expression(expressions)

  def match(self, string: str) -> dict:
    groups = Groups()
    status = self._expressions.match(Cursor(string), groups)

    return { 'status': status, 'groups': groups }