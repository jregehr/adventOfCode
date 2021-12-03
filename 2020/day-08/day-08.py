import re
import sys
import csv

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

# Read in the file
with open(file) as f:
  lines = [line.strip().split(' ') for line in f]

for line in lines:
  line.append(False)
# print(lines)
print(f'Loaded {len(lines)} lines.')

pointer = 0
accumulator = 0
iterations = 0

while True:
  iterations += 1

  if lines[pointer][2]:
    print(f'Reached an infinite loop condition on step {iterations}, position {pointer}. Accumulator value is {accumulator}.')
    # for line in lines:
    #   print(line)
    sys.exit()

  lines[pointer][2] = True
  instruction = lines[pointer][0]
  instructionValue = lines[pointer][1]

  print(f'Pointer {pointer}: {lines[pointer]}')

  if instruction == "acc":
    accumulator += int(instructionValue)
  elif instruction == "jmp":
    pointer += int(instructionValue)
    continue

  # nop
  pointer += 1
