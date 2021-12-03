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


def updateCounts(count, sum):
  sum += count
  return sum


sum = 0

currentCount = {}
for x in range(len(lines)):
  if lines[x] == '':
    # reset
    sum = updateCounts(len(currentCount), sum)
    currentCount = {}

  for y in range(len(lines[x])):
    currentCount[lines[x][y]] = 1

  if x == len(lines) - 1:
    sum = updateCounts(len(currentCount), sum)

print(f'Sum = {sum}')
