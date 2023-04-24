from .__packages__ import Status
from .__packages__ import Matchable

from .Quantifier import Quantifier

class AtLeastQuantifier(Quantifier):
  def __init__(self, expression: Matchable, length: int):
    super().__init__(expression)
    self._length = length

  def get_status_from_count(self, count: int) -> Status:
    return [Status.FALSE, Status.TRUE][int(count >= self._length)]