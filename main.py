from regexp import quantifiers, matchers, symbols, operators, groups
from regexp import RegularExpression, Expression, Matchable
from cursor import Cursor

# @TODO: Переделать архитектуру (Matchable)
# Matchable.match(Cursor, Groups) -> Matchable.match(RegexpDriver)
# Использовать для RegexpDriver шаблон Command (передача все команд ему - это нужно для инверсии зависимости)
# Плюсы такого решения:
# 1) Избавление от большого множества зависимостей
# 2) Нам неважно внутреннее строение наших зависимостей и их состояние, поскольку это контролирует сам driver

# Для создания команд (Command) использовать шаблон Static Fabric (статическая фабрика)
# В той фабрике объекты будут создаваться
# Переименовать: Groups -> Memory
# Разложить: Memory -> (в) Memory, MemoryFrame (Frame)

# Сделать @dataclass Token

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

# (["'])([^"']*)(\0)
expression = RegularExpression([
  groups.Ordered([ matchers.Sequence([ '"', '\'' ]) ]),
  groups.Ordered([ quantifiers.AtLeastZero(matchers.NonSequence([ '"', '\'' ])) ]),
  groups.Ordered([ matchers.Reference('0') ]),
  symbols.Terminate()
])

# ----------------------------------------------------------------------------------

space = matchers.Sequence([ '\t', '\n', '\r', '\v', ' ' ])
multi_space: Matchable = quantifiers.AtLeastZero(space)

def multiline_expression(regular_expression: list[Matchable]) -> Matchable:
  return quantifiers.AtLeastOnce(
    Expression([
      multi_space,
      Expression(regular_expression),
      multi_space
    ])
  )

def read_in_brackets_by_delimiter(brackets: tuple[str, str], delimiter: str) -> Matchable:
  return Expression([
    quantifiers.AtLeastZero(
      groups.Ordered([
        groups.NonCapture(multi_space),
        quantifiers.AtLeastOnce(matchers.NonSequence([delimiter, brackets[1]])),
        groups.NonCapture(
          Expression([
            multi_space,
            matchers.Substring(delimiter),
            multi_space
          ])
        )
      ])
    ),
    groups.Ordered([
      groups.NonCapture(multi_space),
      quantifiers.AtLeastZero(matchers.NonSequence([brackets[1], ' ', '\t', '\n', '\v', '\r'])),
      groups.NonCapture(multi_space)
    ]),
  ])

# ----------------------------------------------------------------------------------

identifier = Expression([
  quantifiers.AtLeastOnce(
    operators.Or([
      matchers.Range('A', 'Z'),
      matchers.Range('a', 'z'),
      matchers.Range('0', '9'),
      matchers.Substring('_')
    ])
  )
])

function_assignation_parser = multiline_expression([
  groups.Separate(
    Expression([
      matchers.Substring('function'),
      multi_space,
      groups.Named('function_name', [ identifier ]),
      multi_space,
      matchers.Substring('('),
      multi_space,
      read_in_brackets_by_delimiter(('(', ')'), ','),
      multi_space,
      matchers.Substring(')'),
      multi_space,
      matchers.Substring('{'),
      multi_space,
      read_in_brackets_by_delimiter(('{', '}'), ';'),
      multi_space,
      matchers.Substring('}')
    ])
  )
])

variables_parser = multiline_expression([
  groups.Separate(
    Expression([
      groups.Named('variable_name', [
        identifier,
        groups.NonCapture(
          Expression([
            multi_space,
            matchers.Substring('=')
          ])
        )
      ]),
      multi_space,
      groups.Named('variable_value', [ quantifiers.AtLeastOnce(matchers.NonSequence([ ';' ])) ]),
      matchers.Substring(';')
    ])
  )
])

callee_parser = multiline_expression([
  groups.Separate(
    Expression([
      groups.Named('callee_name', [
        identifier,
        groups.NonCapture(
          Expression([
            multi_space,
            matchers.Substring('('),
            multi_space
          ])
        )
      ]),
      read_in_brackets_by_delimiter(('(', ')'), ','),
      matchers.Substring(')')
    ])
  )
])

language_parser = quantifiers.AtLeastOnce(
  operators.Or([
    callee_parser,
    function_assignation_parser,
    variables_parser
  ])
)

# ----------------------------------------------------------------------------------

expression_input = '''
  function add(x, y) {
    a = x + y;
    b = x * y;
    return a + b;
  }
  
  x = 1;
  y = 2;
  
  add(x, y)
  add(x - 1, y + 1)
'''

language = RegularExpression([ language_parser ])

import json
print(
  json.dumps(
    parse('let[\t\n\r\v]*(?<name>[a-zA-Z0-9_]+)[\t\n\r\v]*=[\t\n\r\v]*(?<value>[^;]+);'),
    indent=2,
    sort_keys=True
  )
)
print(language.match(expression_input))