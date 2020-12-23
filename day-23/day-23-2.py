import re
import sys
import csv
import math
import copy

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

# print(f'Loading {file}')

# Read in the file
with open(file) as f:
  lines = [line.strip() for line in f]

print(lines)
print(f'Loaded {len(lines)} lines.')


#region Debug Printers

def debug_print(phase, output):
  if debug <= phase:
    print(output)


LINE_BREAK = '================================================'


def debug_line_break(phase):
  debug_print(phase, LINE_BREAK)

#endregion


##############################################
debug = 1
##############################################

#region Data Loading

cups = []
for cup in range(len(lines[0])):
  cups.append(int(lines[0][cup]))

for x in range(10, 1000001):
  cups.append(x)

# debug_print(1, 'starting values')
# debug_print(1, cups)

#endregion

#region functions


def pop3(cups, currentCup):
  result = []
  for x in range(1, 4):
    pop = currentCup + 1
    if pop >= len(cups):
      pop = 0
    result.append(cups.pop(pop))

  return result


def insert(cups, currentCupLabel, to_move):
  targetLabel = currentCupLabel - 1
  while True:
    try:
      position = cups.index(targetLabel)
      break
    except ValueError:
      targetLabel -= 1
      if targetLabel < 1:
        targetLabel = 9
  # print(f'destination: {cups[position]}')
  if position == len(cups) - 1:
    # print('append 3')
    for x in range(len(to_move)):
      cups.append(to_move[x])
  else:
    for x in range(len(to_move)):
      # print(f'insert at {position + x + 1}')
      cups.insert(position + x + 1, to_move[x])


def move_current_cup(cups, currentCupLabel):
  position = cups.index(currentCupLabel)
  newCurrentCup = position + 1
  if newCurrentCup >= len(cups):
    return 0

  return newCurrentCup

 #endregion


currentCup = 0
for move in range(0, 10000000):
  if move % 10000 == 0:
    print(f'move {move}')
  # print(f'\n-- move {move+1} --')
  # print(f'cur={cups[currentCup]}; cups: ', end='')
  currentCupLabel = cups[currentCup]
  # print(*cups, sep=', ')
  # print(f'current: {cups[currentCup]}')
  to_move = pop3(cups, currentCup)
  # print(f'pick up: ', end='')
  # print(*to_move, sep=', ')
  if currentCup >= len(cups):
    currentCup = len(cups) - 1
  insert(cups, currentCupLabel, to_move)
  currentCup = move_current_cup(cups, currentCupLabel)

# debug_print(1, 'ending values')
# print(cups)
# debug_line_break(99)
# print(cups)
# print(to_move)

cupOne = cups.index(1)
print(f'after 1,000,000 rounds, the cups after 1 are: {cups[cupOne+1]} and {cups[cupOne+2]}, multiplied: {cups[cupOne+1] * cups[cupOne+2]}')


# debug_line_break(99)
# print(cups)
# print(f'currentCup = {currentCup}')
