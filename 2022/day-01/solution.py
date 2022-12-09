import sys
import collections

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

## Read in the file
with open(file) as f_input:
  lines = [line.strip() for line in f_input]


# print(lines)
print(f'Loaded {len(lines)} lines.')

# prep variables
elves = dict()
elfCounter = 1

for l in lines:
  # print(f'line: {l}; length:{len(l)}')
  if len(l) == 0:
    elfCounter += 1
    continue

  currentCalories = elves.get(elfCounter, 0) + int(l)
  # print(f'Elf {elfCounter}: {l}, total {currentCalories}')
  elves[elfCounter] = currentCalories


sortedElves = sorted(elves, key=elves.get, reverse=True)
# print(f'elves: {elves}')
# print(f'sorted: {sortedElves}')
      
print(f'Most caloric elves: {sortedElves[0]}:{elves[sortedElves[0]]}, {sortedElves[1]}:{elves[sortedElves[1]]}, and {sortedElves[2]}:{elves[sortedElves[2]]}')
print(f'Total calories: {elves[sortedElves[0]] + elves[sortedElves[1]] + elves[sortedElves[2]]} calories.')

