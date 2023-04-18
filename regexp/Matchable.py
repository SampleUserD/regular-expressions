from .__types__ import Cursor
from .__types__ import Status
from .Groups import Groups

class Matchable:
  def match(self, cursor: Cursor, groups: Groups) -> Status:
    raise Exception('You should implement Matcher.match(cursor: Cursor)')