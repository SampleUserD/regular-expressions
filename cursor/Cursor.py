class Cursor:
  def __init__(self, string: str):
    self._string = string
    self._index = 0
    self._history = []

  def next(self):
    if self.index < self.length:
      self._index += 1

  def lookup(self, offset: int):
    if offset < 0:
      raise Exception('Bad argument passed: expected offset to be non-negative')

    if self.index + offset < self.length:
      return self._string[self.index + offset]
    else:
      return str()

  def slice(self, start: int, end: int):
    return self._string[start:end:1]

  def save(self): self._history.append(self._index)
  def restore(self): self._index = self._history.pop()
  def discard(self): self._history.pop()

  @property
  def current(self): return self._string[self._index]

  @property
  def index(self): return self._index

  @property
  def length(self): return len(self._string)

  @property
  def done(self): return self.index >= self.length