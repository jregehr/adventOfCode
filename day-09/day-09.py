import re
import sys
import csv

if len(sys.argv) != 3:
  sys.exit('Please pass the file name and preamble size as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

# Read in the file
with open(file) as f:
  lines = [int(line.strip()) for line in f]


# print(lines)
print(f'Loaded {len(lines)} lines.')

preamble = int(sys.argv[2])
lookback = preamble
count = 0

for line in lines:
  count += 1

  if count <= preamble:
    continue

  print(f'Testing {line} ...')

  goodValue = False
  for x in range(count - (lookback + 1), count - 1):
    for y in range(x+1, count - 1):
      # print(f'x,y = {x},{y}; {lines[x]},{lines[y]}')
      if (lines[x] + lines[y]) == line:
        goodValue = True
        break

  if not goodValue:
    print(f'Item {count} is not valid: {line}')
    break

print(f'\n\nFinding contiguous numbers that add up to our invalid number\n\n')

targetnumber = lines[count-1]

for start in range(0, len(lines)-1):

  thesum = 0
  least = 99999999999999999
  greatest = 0

  for roll in range(start, len(lines)):
    num = int(lines[roll])
    if num < least:
      least = num

    if num > greatest:
      greatest = num

    thesum += num

    if thesum < targetnumber:
      continue

    if thesum == targetnumber:
      print(f'started at {start}, got to {roll}, sum matches {targetnumber}. Least: {least}; greatest: {greatest}, sum is {least + greatest}')
      sys.exit()
    
    break
