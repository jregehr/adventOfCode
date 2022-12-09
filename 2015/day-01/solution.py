import sys

if len(sys.argv) != 2:
  sys.exit('Please pass the instructions an argument.')

instructions = sys.argv[1]

up = instructions.count('(')
down = instructions.count(')')
arrived = up - down

print(f'Arrived at floor {arrived}')


x = 0
floor = 0
for char in instructions:
  x += 1
  if char == "(":
    floor += 1
  else:
    floor -= 1
  if floor < 0:
    break

print(f'Position of the character that causes Santa to first enter the basement: {x}')