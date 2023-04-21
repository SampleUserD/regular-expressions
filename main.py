from model import quantifiers, matchers, symbols, operators, groups
from model import RegularExpression, Expression, Matchable

# Переделать _libraries.event: Manager и Scheduler

# @TODO: Переделать архитектуру (Matchable)
# Matchable.match(Cursor, Groups) -> Matchable.match(RegexpDriver)
# Использовать для RegexpDriver шаблон Command (передача все команд ему - это нужно для инверсии зависимости)
# Плюсы такого решения:
# 1) Избавление от большого множества зависимостей
# 2) Нам неважно внутреннее строение наших зависимостей и их состояние, поскольку это контролирует сам executor

# Для создания команд (Command) использовать шаблон Static Fabric (статическая фабрика)
# В той фабрике объекты будут создаваться
# Переименовать: Groups -> Memory
# Разложить: Memory -> (в) Memory, MemoryFrame (Frame)

# Сделать @dataclass Token

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

print(language.match(expression_input))