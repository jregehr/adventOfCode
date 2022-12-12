import sys
import math
import queue
import decimal
from math import lcm

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

# file = sys.argv[1]

# print(f'Loading {file}')

# ## Read in the file
# with open(file) as f_input:
#   lines = [line.strip() for line in f_input]


# # print(lines)
# print(f'Loaded {len(lines)} lines.')

# prep variables

# region Monkey

class Monkey:
  def __init__(self, monkeyNum, items, action, testDivisor, trueThrow, falseThrow):
    self._items = queue.Queue()
    self._action = action # eval('lambda old: ' + action)
    self._testDivisor = testDivisor
    self._trueThrow = trueThrow
    self._falseThrow = falseThrow
    self._inspections = 0
    self._monkeyNum = monkeyNum
    for i in items:
      self._items.put(i)

  @property
  def items(self):
    return self._items

  @property
  def inspections(self):
    return self._inspections
  
  @property
  def divider(self):
    return self._testDivisor

  def inspectTestThrow(self, monkeys, limiter):
    if self._items.empty():
      # nothing to inspect
      return
    while not self._items.empty():
    # for i in range(0, len(self._items)):
      self._inspections += 1
      old = self._items.get()
      item = eval(self._action)
      # item = self._action(old)
      # item = int(math.floor(new/3))
      # num = item / self._testDivisor
      # if num.is_integer():
      # if math.fmod( decimal.Decimal(item), decimal.Decimal(self._testDivisor)) == 0:
        # decimal.
      if item > limiter:
        item = item % limiter
      dd = item % self._testDivisor
      # x = ""
      # if dd == 0:
      #   x="!!!!!!!!!!!!!!!!!!!"
      #   # print(f'M{self._monkeyNum}: insp#{self._inspections}; old{old} --> new{item} -- d{self._testDivisor} % {dd}{x}')
      #   # print(f'M{self._monkeyNum}: insp#{self._inspections}; d{self._testDivisor} % {dd}{x}')
      #   print(f'M{self._monkeyNum}')#: insp#{self._inspections}')

      # if item % self._testDivisor == 0:
      if dd == 0:
        monkeys[self._trueThrow].items.put(item)
      else:
        monkeys[self._falseThrow].items.put(item)


# endregion

monkeys = [
  # Monkey(0, [79, 98],         "old * 19",  23, 2, 3),
  # Monkey(1, [54, 65, 75, 74], "old + 6",   19, 2, 0),
  # Monkey(2, [79, 60, 97],     "old * old", 13, 1, 3),
  # Monkey(3, [74],             "old + 3",   17, 0, 1)
  Monkey(0, [92, 73, 86, 83, 65, 51, 55, 93], "old * 5", 11, 3, 4),
  Monkey(1, [99, 67, 62, 61, 59, 98], "old * old", 2, 6, 7),
  Monkey(2, [81, 89, 56, 61, 99], "old * 7", 5, 1, 5),
  Monkey(3, [97, 74, 68], "old + 1", 17, 2, 5),
  Monkey(4, [78, 73], "old + 3", 19, 2, 3),
  Monkey(5, [50], "old + 5", 7, 1, 6),
  Monkey(6, [95, 88, 53, 75], "old + 8", 3, 0, 7),
  Monkey(7, [50, 77, 98, 85, 94, 56, 89], "old + 2", 13, 4, 0),
]

limiter = lcm(*[monkey.divider for monkey in monkeys])

for round in range(1,10001):
  if round % 50 == 0:
    print(f"Round {round}")
# for round in range(1,10001):
#   # print(f"Round {round} =====================================")
  for monkey in monkeys:
    monkey.inspectTestThrow(monkeys, limiter)

monkeyInspections = [0]*len(monkeys)

for i in range(0,len(monkeys)):
  monkey = monkeys[i]
  print(f"Monkey {i} inspected items {monkey.inspections} times.")
  monkeyInspections[i] = monkey.inspections
monkeyInspections.sort(reverse=True)

print(f"Monkey business: {monkeyInspections[0]*monkeyInspections[1]}")

