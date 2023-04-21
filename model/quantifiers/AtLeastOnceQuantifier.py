from .__types__ import Status
from .__types__ import Matchable

from .Quantifier import Quantifier

class AtLeastOnceQuantifier(Quantifier):
  def __init__(self, expression: Matchable):
    super().__init__(expression)

  def get_status_from_count(self, count: int) -> Status:
    return [Status.FALSE, Status.TRUE][int(count >= 1)]