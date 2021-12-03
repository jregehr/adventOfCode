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

  ## Splitting 2-9 c: ccccccccc
  things = re.split('-| |: ', l)
  pos1 = int(things[0])-1
  pos2 = int(things[1])-1
  target = things[2]
  char1 = things[3][pos1]
  char2 = things[3][pos2]

  if char1 != char2 and (target == char1 or target == char2):
    validity = 'valid'
    validCount += 1
  else:
    invalidCount += 1
    validity = 'invalid'
  # print(f'{l} is {validity}, target is {target}; char1 = {char1} and char2 = {char2}')

print(f'I found {validCount} valid and {invalidCount} invalid passwords.')
