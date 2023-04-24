from .__packages__ import Status
from .__packages__ import Matchable

from .Quantifier import Quantifier

class AtLeastZeroQuantifier(Quantifier):
  def __init__(self, expression: Matchable):
    super().__init__(expression)

  def get_status_from_count(self, count: int) -> Status:
    return [Status.FALSE, Status.TRUE][int(count >= 0)]