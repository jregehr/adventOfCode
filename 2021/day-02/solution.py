import sys

if len(sys.argv) != 2:
  sys.exit('Please pass the file name as an argument.')

file = sys.argv[1]

print(f'Loading {file}')

## Read in the file
with open(file) as f_input:
  lines = f_input.readlines()

# print(lines)
print(f'Loaded {len(lines)} lines.')

hpos = 0
dpos = 0

for l in lines:
  directive = l.split()
  # print(f'directive: {directive}')
  if directive[0] == 'forward':
    hpos += int(directive[1])
  elif directive[0] == 'down':
    dpos += int(directive[1])
  else:
    dpos += -1*int(directive[1])

print(f'Part 1: Final H Position: {hpos}; depth {dpos}. Multiplied: {hpos*dpos}')

realHPos = 0
realDepth = 0
aim = 0

for l in lines:
  directive = l.split()
  print(f'directive: {directive}')
  if directive[0] == 'forward':
    realHPos += int(directive[1])
    realDepth += aim * int(directive[1])
  elif directive[0] == 'down':
    aim += int(directive[1])
  else:
    aim += -1*int(directive[1])

print(f'Part 2: Final H Position: {realHPos}; depth {realDepth}. Aim: {aim} Multiplied: {realHPos*realDepth}')
