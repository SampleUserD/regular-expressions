from .__packages__ import Executor
from .status import Status

class Matchable:
  def match(self, executor: Executor) -> Status:
    raise Exception('You should implement Matcher.match(executor: Executor)')