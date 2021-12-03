import re
import sys
import csv

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

# Read in the file
with open(file) as f:
  lines = [line.strip()*333 for line in f]

# print(lines)
# for l in lines:
  # print(l)
print(f'Loaded {len(lines)} lines.')

jumps = [
    [1, 1],
    [3, 1],
    [5, 1],
    [7, 1],
    [1, 2],
]

treeTotal = 1

for jumpset in jumps:

  position = 0
  treeCount = 0
  jump = jumpset[0]
  lineJump = jumpset[1]
  lineCount = 0

  for l in lines:
    lineCount += 1
    # print(f'line {lineCount} should skip: {lineCount % lineJump}')
    if lineJump > 1 and lineCount % lineJump == 0:
      continue

    if l[position] == "#":
      treeCount += 1

    position += jump

  print(f'Encountered {treeCount} trees for {jumpset}')

  treeTotal = treeTotal * treeCount

print(f'The final total is {treeTotal}')
