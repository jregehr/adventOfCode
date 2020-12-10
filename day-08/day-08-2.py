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


def reset():
  for line in lines:
    line[2] = False


def runit():
  pointer = 0
  accumulator = 0
  iterations = 0

  while True:
    iterations += 1

    if pointer >= len(lines):
      print(f'Program terminates after {iterations} iterations, position {pointer}. Accumulator value is {accumulator}.')
      return True

    if lines[pointer][2]:
      print(f'Reached an infinite loop condition on step {iterations}, position {pointer}. Accumulator value is {accumulator}.')
      # for line in lines:
      #   print(line)
      return False

    lines[pointer][2] = True
    instruction = lines[pointer][0]
    instructionValue = lines[pointer][1]

    # print(f'Pointer {pointer}: {lines[pointer]}')

    if instruction == "acc":
      accumulator += int(instructionValue)
    elif instruction == "jmp":
      pointer += int(instructionValue)
      continue

    # nop
    pointer += 1


attempts = 0

# Loop through the input, changing one line at a time.
for line in lines:
  reset()
  if line[0] == "acc":
    continue

  attempts += 1
  print(f'Attempt {attempts}')

  if line[0] == "nop":
    line[0] = "jmp"
    result = runit()
    if result:
      print(f'Success on attempt {attempts}.')
      sys.exit()
    else:
      line[0] = "nop"

  if line[0] == "jmp":
    line[0] = "nop"
    result = runit()
    if result:
      print(f'Success on attempt {attempts}.')
      sys.exit()
    else:
      line[0] = "jmp"

print('No successful change was found.')
