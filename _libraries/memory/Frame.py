from typing import Generic, TypeVar

from .ReservationMode import ReservationMode

Value = TypeVar('Value')

class Frame(Generic[Value]):
  def __init__(self):
    self._orderedGroups: list[Value] = []
    self._namedGroups: dict[str, Value] = {}

  def add(self, value: Value, **kwargs) -> None:
    if ('group_type' not in kwargs) or ('group_name' not in kwargs):
      raise Exception('Bad arguments passed: group_type and group_name expected')

    if not isinstance(kwargs['group_type'], ReservationMode):
      raise Exception('Bad argument passed: group_type should be type of GroupTypes')

    if not isinstance(kwargs['group_name'], str):
      raise Exception('Bad argument passed: group_name should be type of string (str)')

    group_type: ReservationMode = kwargs['group_types']
    group_name: str = kwargs['group_name']

    if group_type == ReservationMode.ORDERED: self._orderedGroups.append(value)
    if group_type == ReservationMode.NAMED: self._namedGroups[group_name] = value

  def get(self, name: str) -> Value:
    if name.isnumeric(): return self._orderedGroups[int(name)]
    else: return self._namedGroups[name]

  @property
  def reserves(self):
    ordered_groups = { index: self._orderedGroups[index] for index in range(0, len(self._orderedGroups)) }
    named_groups = self._namedGroups

    return named_groups | ordered_groups