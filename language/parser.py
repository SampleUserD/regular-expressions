from _libraries.cursor import Cursor

def matches(cursor: Cursor, character: str) -> bool:
  """
  Moves cursor if character matches the current

  :param cursor: Cursor to string
  :param character: Character you need to match
  :returns: Character matches the current or not
  """
  if cursor.current == character:
    cursor.next()
    return True

  return False

def character_token(sub_type: str, value: str):
  return { 'type': f'CHARACTER.{sub_type.upper()}', 'value': value }

def sequence_token(sub_type: str, value):
  return { 'type': f'SEQUENCE.{sub_type.upper()}', 'value': value }

def range_token(sub_type: str, value):
  return { 'type': f'RANGE.{sub_type.upper()}', 'value': value }

def group_token(sub_type: str, name: str, expression: list):
  return { 'type': f'GROUP.{sub_type.upper()}', 'value': { 'name': name, 'expression': expression } }

def quantifier_token(sub_type: str, expression):
  return { 'type': f'QUANTIFIER.{sub_type.upper()}', 'value': expression }

reserved_symbols = ['\\', '.', '[', ']', '(', ')', '{', '}', '^', '|', '*', '+', '?']

def parse(regular_expression: str):
  cursor = Cursor(regular_expression)
  syntax_tree = []

  while not cursor.done:
    if matches(cursor, '\\'):
      syntax_tree.append(character_token('escaped', cursor.current))
      cursor.next()
    elif matches(cursor, '.'):
      syntax_tree.append(character_token('any', '.'))
    elif matches(cursor, '['):
      sequence = []
      inversion = False

      if matches(cursor, '^'):
        inversion = True

      while cursor.current != ']' and (not cursor.done):
        if matches(cursor, '\\'):
          sequence.append(character_token('escaped', cursor.current))
          cursor.next()
          continue

        if cursor.lookup(1) == '-':
          start = character_token('substring', cursor.current)
          cursor.next()
          cursor.next()
          end = character_token('substring', cursor.current)
          cursor.next()

          sequence.append(range_token('common', [ start, end ]))
          continue

        substring = str()

        while (cursor.lookup(1) != '-') and (cursor.current != '\\') and (cursor.current != ']'):
          substring += cursor.current
          cursor.next()

        sequence.append(character_token('substring', substring))

      cursor.next()

      if inversion:
        syntax_tree.append(sequence_token('inversion', sequence))
      else:
        syntax_tree.append(sequence_token('common', sequence))
    elif matches(cursor, '('):
      sub_type = 'ordered'
      name = str()

      # Очевидно, что это state-машина
      if matches(cursor, '?'):
        if matches(cursor, ':'):
          sub_type = 'expression'
        if matches(cursor, '<'):
          sub_type = 'named'

          while cursor.current != '>':
            name += cursor.current
            cursor.next()

          cursor.next()
        if matches(cursor, '\''):
          sub_type = 'named'

          while cursor.current != '\'':
            name += cursor.current
            cursor.next()

          cursor.next()

      level = 0
      sub_expression = str()

      while True:
        if cursor.current == '(': level += 1
        if cursor.current == ')': level = max(0, level - 1)

        sub_expression += cursor.current
        cursor.next()

        if cursor.done or ((cursor.current == ')') and (level == 0)): break

      syntax_tree.append(group_token(sub_type, name, parse(sub_expression)))
    elif matches(cursor, '+'):
      syntax_tree[len(syntax_tree) - 1] = quantifier_token('at_least_once', syntax_tree[len(syntax_tree) - 1])
    elif matches(cursor, '*'):
      syntax_tree[len(syntax_tree) - 1] = quantifier_token('at_least_zero', syntax_tree[len(syntax_tree) - 1])
    elif matches(cursor, '?'):
      syntax_tree[len(syntax_tree) - 1] = quantifier_token('at_most_once', syntax_tree[len(syntax_tree) - 1])
    else:
      substring = str()

      while (not cursor.done) and (cursor.current not in reserved_symbols):
        substring += cursor.current
        cursor.next()

      if substring != str():
        syntax_tree.append(character_token('substring', substring))

      cursor.next()

  return syntax_tree