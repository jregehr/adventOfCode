import re
import sys
import csv

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

# Read in the file
with open(file) as f:
  lines = [line.strip() for line in f]

# print(lines)
print(f'Loaded {len(lines)} lines.')

BRACKET_RE = re.compile(r'\(([^\(\)]+)\)')
OPNUM_RE = re.compile(r'[\+\*] [0-9]+')
START_RE = re.compile(r'^[0-9]+ ')
NEW_PLUS_RE = re.compile(r'[0-9]+ [\+ 0-9+]+')


# def parse_bracketed_expression(expression):
#   # print('=== parse_bracketed_expression =================================================')
#   # print(f'{expression} becomes {expression[1:-1]}')
#   return parse_expression(expression[1:-1])


# def parse_expression(expression):
#   # print('=== parse_expression ===========================================================')
#   # print(f'recieved {expression}')

#   unbracketedExpression = expression
#   brackets = BRACKET_RE.search(unbracketedExpression)
#   while brackets is not None:
#     answer = parse_bracketed_expression(brackets.group(0))
#     # print(brackets.group(0))
#     unbracketedExpression = unbracketedExpression[0:brackets.start()] + str(answer) + unbracketedExpression[brackets.end():]
#     # print(unbracketedExpression)
#     brackets = BRACKET_RE.search(unbracketedExpression)

#   # print(f'Unbracketed is now {unbracketedExpression}')

#   finalExpression = START_RE.match(unbracketedExpression).group(0)
#   for item in OPNUM_RE.findall(unbracketedExpression):
#     finalExpression = f'( {finalExpression} {item} ) '

#   # print(f'Final Expression: {finalExpression}')
#   return eval(finalExpression)

class HiAdd:
  def __add__(self, other):
    return self + other

  def __matmul__(self, other):
    return self + other


class HiAdd2:
  def __init__(self, num):
    self._num = int(num)

  def __sub__(self, other):
    # print(f'self:{self}; self.myNum={self._num}')
    # print(f'other:{other}; other.myNum={other.num}')
    # sNum = self._num
    # oNum = other.num
    # print(f'got sNum={sNum} and oNum={oNum}')
    return HiAdd2(self.num * other.num)

  def __mul__(self, other):
    # print(f'self:{self}; self.myNum={self._num}')
    # print(f'other:{other}; other.myNum={other.num}')
    # sNum = self._num
    # oNum = other.num
    # print(f'got sNum={sNum} and oNum={oNum}')
    return HiAdd2(self.num + other.num)

  @property
  def num(self):
    return self._num


def debug_print(output):
  if debug:
    print(output)


def parse_bracketed_expression_new_rules(expression):
  debug_print('=== parse_bracketed_expression_new_rules =================================================')
  debug_print(f'{expression} becomes {expression[1:-1]}')
  return parse_expression_new_rules(expression[1:-1])


def parse_expression_new_rules(expression):
  debug_print('=== parse_expression_new_rules ===========================================================')
  debug_print(f'recieved {expression}')

  unbracketedExpression = expression
  brackets = BRACKET_RE.search(unbracketedExpression)
  while brackets is not None:
    debug_print(f'Found Brackets: {brackets.group(0)}')
    answer = parse_bracketed_expression_new_rules(brackets.group(0))
    unbracketedExpression = unbracketedExpression[0:brackets.start()] + str(answer) + unbracketedExpression[brackets.end():]
    debug_print(f'Unbracketed: {unbracketedExpression}')
    brackets = BRACKET_RE.search(unbracketedExpression)

  debug_print(f'Unbracketed is now {unbracketedExpression}')

  debug_print(NEW_PLUS_RE.findall(unbracketedExpression))
  # sys.exit()
  for item in NEW_PLUS_RE.findall(unbracketedExpression):
    unbracketedExpression = unbracketedExpression.replace(item, f'({item.replace(" ","")})', 1)

  debug_print(f'Final Expression: {unbracketedExpression}')
  return eval(unbracketedExpression)


def parse_expression_hack(expression):
  debug_print(f'Received: {expression}')
  # firstReplace = expression.replace('+', '@')
  # secondReplace = re.sub(r'([0-9]+)', r'HiAdd(\1)', firstReplace)
  # debug_print(secondReplace)
  relE = re.sub(r'([0-9]+)', r'HiAdd2(\1)', expression).replace("*", "-").replace("+", "*")
  debug_print(relE)
  return eval(relE)
  # return eval(firstReplace)


finalSumOldRules = 0
finalSumNewRules = 0
finalSumHackRules = 0

# for x in lines:
#   answer = parse_expression(x)
#   print(f'Old Rules: [{x}] evaluates to {answer}')
#   finalSumOldRules += answer
# print(f'Final answer Under the NEW rules: {finalSumOldRules}')

debug = False

for x in lines:
  answer = parse_expression_new_rules(x)
  print(f'New Rules: [{x}] evaluates to {answer}')
  finalSumNewRules += answer
print(f'Final answer Under the NEW rules: {finalSumNewRules}')

print('=========================================================')

for x in lines:
  answer = parse_expression_hack(x)
  print(f'Hack Rules: [{x}] evaluates to {answer.num}')
  finalSumHackRules += answer.num
print(f'Final answer Under the Hack rules: {finalSumHackRules}')
