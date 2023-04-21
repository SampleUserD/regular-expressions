class Groups:
  frames: list[tuple[list[str], dict[str, str]]] = []

  def create_frame(self): self.frames.append(([], {}))

  def remove_frame(self):
    if len(self.frames) > 0:
      self.frames.pop()

  def add_ordered(self, string: str) -> None:
    if len(self.frames) == 0: self.create_frame()
    self.frame[0].append(string)

  def add_named(self, name: str, string: str) -> None:
    if len(self.frames) == 0: self.create_frame()
    if name in self.frame[1]: self.create_frame()
    self.frame[1][name] = string

  def get(self, name: str):
    if name.isnumeric():
      return self.frame[0][int(name)]
    else:
      return self.frame[1][name]

  @property
  def frame(self):
    return self.frames[len(self.frames) - 1]

  @property
  def groups(self):
    return map(
      lambda frame: self.frame[1] | { index: self.frame[0][index] for index in range(0, len(self.frame[0])) },
      self.frames
    )