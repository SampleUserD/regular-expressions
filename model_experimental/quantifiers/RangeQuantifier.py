from .__packages__ import Status
from .__packages__ import Matchable

from .Quantifier import Quantifier

class RangeQuantifier(Quantifier):
  def __init__(self, expression: Matchable, span: range):
    super().__init__(expression)
    self._span = range(span.start, span.stop + 1)

  def get_status_from_count(self, count: int) -> Status:
    return [Status.FALSE, Status.TRUE][int(count in self._span)]