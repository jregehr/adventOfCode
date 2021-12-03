import sys

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

## Read in the file
with open(file) as f_input:
  lines = list(f_input.read().split())

# print(lines)
print(f'Loaded {len(lines)} lines.')

previous = 999999
increasedCount = 0

for l1 in lines:
  depthnum = int(l1)
  if depthnum > previous:
    increasedCount += 1
  previous = depthnum

print(f'Part 1: Of {len(lines)} readings, {increasedCount} were deeper than the previous reading.')

print(f'')
print(f'')

previousSum = 9999999
increasedSumCount = 0

for index, line in enumerate(lines):
  if index < 2:
    continue
  depthSum = int(lines[index-2]) + int(lines[index-1]) + int(lines[index])
  # print(f'Line {index}: {line}; sum={depthSum}')
  if depthSum > previousSum:
    increasedSumCount += 1
  previousSum = depthSum

print(f'Part 2: Of {len(lines)} sums, {increasedSumCount} were deeper than the previous sum.')