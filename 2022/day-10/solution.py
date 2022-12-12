import sys

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
interestingStrengths = {
  20: 0,
  60: 0,
  100: 0,
  60: 0,
  100: 0,
  140: 0,
  180: 0,
  220: 0
}

cycleCount = 1
instructionCount = 0
instructionValue = 0
xRegister = 1

screen = [None] * 241

for l in lines:
  # print(f'instructionSet: {l}')
  instructionSet = l.split(" ")
  if instructionSet[0] == "addx":
    instructionCount = 2
    instructionValue = int(instructionSet[1])
  else:
    instructionCount = 1
    instructionValue = 0
  
  for i in range(0, instructionCount):
    if (xRegister - 1) <= ((cycleCount % 40 - 1)) <= (xRegister + 1):
      screen[cycleCount] = '#'
    else:
      screen[cycleCount] = '.'
    print(f'cc:{cycleCount} | xr:{xRegister} | sc:{screen[cycleCount]} | inst:{l} ')
    cycleCount += 1
    # print(f'{instructionSet[0]} index {i}, cycle {cycleCount}')
    if interestingStrengths.get(cycleCount) != None:
      interestingStrengths[cycleCount] = cycleCount * xRegister
  
  xRegister += instructionValue

print(f'xRegister: {xRegister} at cycle {cycleCount}')
print(interestingStrengths)
print()
total = 0
for i in interestingStrengths.values():
  total += i

print(f'total interesting signals: {total}')

print('')
print('')
print("".join(screen[  1: 40]))
print("".join(screen[ 41: 80]))
print("".join(screen[ 81:120]))
print("".join(screen[121:160]))
print("".join(screen[161:200]))
print("".join(screen[201:240]))