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


def updateCounts(currentCounts, groupCount, sum):
  print(f'in updateCounts, groupCount={groupCount}, sum={sum}, currentCounts={currentCounts}')
  for count in currentCounts.values():
    if count == groupCount:
      sum += 1
  print(f'returning sum={sum}')
  return sum


sum = 0
groupCount = 0

currentCount = {}
for x in range(len(lines)):
  if lines[x] == '':
    # reset
    # print(currentCount)
    sum = updateCounts(currentCount, groupCount, sum)
    currentCount = {}
    groupCount = 0
    continue

  # print(f'x={x}, line={lines[x]}')

  groupCount += 1
  for y in range(len(lines[x])):
    # print(f'x={x}, y={y}, char={lines[x][y]}')
    if groupCount == 1:
      currentCount[lines[x][y]] = 1
    else:
      theCount = currentCount.get(lines[x][y])
      # print(f'theCount={theCount}')
      if theCount is not None:
        currentCount[lines[x][y]] += 1
  # print(currentCount)
  # catch the last sum
  if x == len(lines) - 1:
    sum = updateCounts(currentCount, groupCount, sum)

print(f'Sum = {sum}')
