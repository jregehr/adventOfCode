import re
import sys
import csv

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

# Read in the file
with open(file) as f:
  lines = [line.strip()*33 for line in f]

# print(lines)
print(f'Loaded {len(lines)} lines.')

jumps = 3
position = 0
treeCount = 0

for l in lines:
  if l[position] == "#":
    treeCount += 1

  position += jumps

print(f'Encountered {treeCount} trees')
