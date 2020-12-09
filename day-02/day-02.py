import re
import sys
import csv

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

## Read in the file
with open(file) as f:
  lines = [line.strip() for line in f]

# print(lines)
print(f'Loaded {len(lines)} lines.')

validCount = 0
invalidCount = 0

for l in lines:
  # print(f'Line={l.strip()}')

  ## Splitting 2-9 c: ccccccccc
  things = re.split('-| |: ', l)
  min = int(things[0])
  max = int(things[1])
  occurrences = things[3].count(things[2])

  if occurrences >= min and occurrences <= max:
    # print(f'{l} is valid, found {things[2]} {occurrences} times. Min was {min}; max was {max}')
    validCount += 1
  else:
    invalidCount += 1
    # print(f'{l} is not valid, found {things[2]} {occurrences} times. Min was {min}; max was {max}')

print(f'I found {validCount} valid and {invalidCount} invalid passwords.')
