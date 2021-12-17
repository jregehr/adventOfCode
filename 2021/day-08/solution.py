import sys

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

## Read in the file
with open(file) as f_input:
  lines = f_input.readlines()

# print(lines)
print(f'Loaded {len(lines)} lines.')

# prep variables
count1478 = 0

for l in lines:
  # print(f'line: {l}')
  digits = l.split('|')[1].split()
  for digit in digits:
    if len(digit) == 7 or len(digit) <= 4:
      count1478 += 1

print(f'There are {count1478} instances of 1, 4, 7, and 8 in the output.')

# 1 - 2 segments
# 4 - 4 segments
# 7 - 3 segments
# 8 - 7 segments

# 2 - 5 segments; not 3 or 5
# 3 - 5 segments; full overlap with 1
# 5 - 5 segments; 3 overlap with 4

# 6 - 6 segments; not 0 or 9
# 0 - 6 segments; full overlap with 1
# 9 - 6 segments; full overlap with 4

def strSort(str):
  return ''.join(sorted(str))

def containsAll(str, set):
  """ Check whether sequence str contains ALL of the items in set. """
  return 0 not in [c in str for c in set]

def countOverlap(str, set):
  overlaps = 0
  for item in set:
    if item in str:
      overlaps += 1
  
  return overlaps

def findDigits(clues):
  # print(f'findDigits starting with {clues}')
  resultByClue = {}
  resultByDigit = {}
  toRemove = set()
  #find easy ones
  for clue in clues:
    sClue = strSort(clue)
    if len(clue) == 7:
      resultByClue[sClue] = 8
      resultByDigit[8] = sClue
      toRemove.add(clue)
    elif len(clue) == 2:
      resultByClue[sClue] = 1
      resultByDigit[1] = sClue
      toRemove.add(clue)
    elif len(clue) == 4:
      resultByClue[sClue] = 4
      resultByDigit[4] = sClue
      toRemove.add(clue)
    elif len(clue) == 3:
      resultByClue[sClue] = 7
      resultByDigit[7] = sClue
      toRemove.add(clue)
  clues = clues - toRemove
  toRemove = set()

  for clue in clues:
    sClue = strSort(clue)
    if len(clue) == 5:
      if containsAll(clue, resultByDigit[1]):
        resultByClue[sClue] = 3
        resultByDigit[3] = sClue
        toRemove.add(clue)
        continue
      if countOverlap(clue, resultByDigit[4]) == 3:
        resultByClue[sClue] = 5
        resultByDigit[5] = sClue
        toRemove.add(clue)
        continue
      resultByClue[sClue] = 2
      resultByDigit[2] = sClue
      toRemove.add(clue)
  clues = clues - toRemove
  toRemove = set()

  for clue in clues:
    sClue = strSort(clue)
    if len(clue) == 6:
      if containsAll(clue, resultByDigit[4]):
        resultByClue[sClue] = 9
        resultByDigit[9] = sClue
        toRemove.add(clue)
        continue
      if containsAll(clue, resultByDigit[1]):
        resultByClue[sClue] = 0
        resultByDigit[0] = sClue
        toRemove.add(clue)
        continue
      resultByClue[sClue] = 6
      resultByDigit[6] = sClue
      toRemove.add(clue)

  clues = clues - toRemove

  if len(clues) > 0:
    print('ALARM! THERE ARE CLUES LEFT')

  # print(f'resultByClue={resultByClue}')
  # print(f'resultByDigit={resultByDigit}')
  return resultByClue#, resultByDigit

finalSum = 0

for l in lines:
# for n in range(2):
  # l = lines[n]
  # print(f'\n\n\nline: {l}')
  cluesAndDigits = l.split('|')
  # print(f'clues as list: {cluesAndDigits[0]}')
  # print(f'clues as set: {set(cluesAndDigits[0].split())}')
  resultByClue = findDigits(set(cluesAndDigits[0].split()))
  intermediateNumber = ''
  for realDigits in cluesAndDigits[1].split():
    # print(f'realDigits: {realDigits}')
    intermediateNumber += f'{resultByClue[strSort(realDigits)]}'
  # print(f'intermediateNumber: {intermediateNumber}')
  finalSum += int(intermediateNumber)

print(f'The sum of all things is {finalSum}')
