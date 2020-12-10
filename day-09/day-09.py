import re
import sys
import csv

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

# Read in the file
with open(file) as f:
  lines = [int(line.strip()) for line in f]


# print(lines)
print(f'Loaded {len(lines)} lines.')


preamble = 25
lookback = 25
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
    sys.exit()
